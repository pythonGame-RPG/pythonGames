from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False
import os
import sys
sys.path.append('../../Display')
sys.path.append('../DTO')
import re
import time
import datetime
import csv
import random
from urllib.request import urlopen
# import requests
from bs4 import BeautifulSoup
import tkinter as tk
from DbAccess import * 
import DTO.names as DTO
from settings import *

class NameDAO():
    def __init__(self):
        self.na = DTO.Name()
        self.ins_name = {}
        self.ins_name['name'] = self.na.name
        self.ins_name['users_num'] = self.na.users_num
        self.ins_name['trend'] = self.na.trend
        self.ins_name['is_deleted'] = self.na.is_deleted
        self.ins_name['version'] = self.na.version
        self.ins_name['ins_date'] = self.na.ins_date
        self.ins_name['ins_id'] = self.na.ins_id
        self.ins_name['upd_date'] = self.na.upd_date
        self.ins_name['upd_id'] = self.na.upd_id

    def insert_name(self,name_list):
        # 取得したname_listを件数分ループ
        for _name in name_list:
            # 名前を取得
            self.ins_name['name'] = _name
            
            dbaccess().INSERT_Column(MST_NAMES, self.ins_name, users_num=1)

    # trendを+1する
    def update_trend(self,name_list):
        # 取得したname_listを件数分ループ
        print('update_trend開始...')
        res = 0
        for _name in name_list:
            sql = 'UPDATE names SET trend = trend + 1 WHERE name = "{}"'.format(_name)
            dbaccess().upins_sql(sql)
            res = res + 1
        print('update_trend：{}件'.format(res))

    # nameを無作為に取得
    def select_randone(self):
        sql = 'SELECT name from names ORDER BY RAND() LIMIT 1'
        return dbaccess().exe_sql(sql)

    # versionを+1する
    def update_version(self,name_list):
        # 取得したname_listを件数分ループ
        print('update_version開始...')
        res = 0
        for _name in name_list:
            sql = 'UPDATE names SET version = version + 1 WHERE name = "{}"'.format(_name)
            dbaccess().upins_sql(sql)
            res = res + 1
        print('登録・更新件数：{}件'.format(res))

    def main(self):
        """
        メイン処理
        """
        # --------------------------------------
        # 作品ページのURLを指定（コメントアウト・コメントインで指定できるようにしています）
        url_list = [
            "https://yomou.syosetu.com/rank/list/type/daily_total/" # 小説を読もう日間ランキング
            ,
            "https://yomou.syosetu.com/rank/list/type/weekly_total/" # 小説を読もう週刊ランキング
            ,
            "https://yomou.syosetu.com/rank/list/type/monthly_total/" # 小説を読もう月間ランキング
                ]
        # --------------------------------------
        # ランキングから開始
        scraping_list = []
        name_list = []
        url = random.choice(url_list)
        bs_obj = self.make_bs_obj(url)
        time.sleep(3)

        # 小説を取得
        novel_list = [a_bs_obj.find("a").attrs["href"] for a_bs_obj in bs_obj.findAll("div", {"class": "rank_h"})]
        time.sleep(3)

        rand_num = random.choices(range(len(novel_list)), k=10)
        for i in rand_num:

            url = novel_list[i]
            bs_obj = self.make_bs_obj(url)
            # ストーリーを取得
            story_list = ["https://ncode.syosetu.com" + a_bs_obj.find("a").attrs["href"] for a_bs_obj in bs_obj.findAll("dd", {"class": "subtitle"})]

            lim_num = 10
            story_num = len(story_list)
            if story_num < 10:
                lim_num = story_num
            rand_num = random.choices(range(len(story_list)), k=lim_num)
        
            for j in rand_num:
                url = story_list[j]
                bs_obj = self.make_bs_obj(url)
                nov_text = self.get_main_text(bs_obj)

                story_name = re.findall('[\u30A1-\u30FF]{2,10}',nov_text)
                name_list.extend(story_name)
                scraping_list.extend(name_list)

                print(story_name)

            # INSERT
            NameDAO().insert_name(name_list)
            # 重複を除去しtrendを設定
            rem_list = list(set(name_list))
            # UPDATE
            NameDAO().update_trend(rem_list)

            name_list = []

        # 重複を除去しtrendを設定
        rem_list = list(set(name_list))
        # UPDATE
        NameDAO().update_version(rem_list)
            
        #save_as_csv(stories, novel_title)

    def make_bs_obj(self, url):
        """
        BeautifulSoupObjectを作成
        """
        html = urlopen(url)
        # html = requests.get(url)
        # content_type_encoding = html.encoding if html.encoding != 'ISO-8859-1' else None
        logger.debug('access {} ...'.format(url))

        # return BeautifulSoup(html,"html.parser",from_encoding=content_type_encoding)
        return BeautifulSoup(html,"html.parser")

    def get_main_text(self, bs_obj):
        """
        各話のコンテンツをスクレイピング
        """
        text = ""
        text_htmls = bs_obj.findAll("div",{"id":"novel_honbun"})[0].findAll("p")

        for text_html in text_htmls:
            text = text + text_html.get_text() + "\n\n"
        
        return text

    def save_as_csv(self, stories, novel_title = ""):
        """
        csvファイルにデータを保存
        """
        # バックアップファイルの保存先の指定    
        directory_name = "novels"
        # ディレクトリが存在しなければ作成する
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)

        # ファイル名の作成
        today = datetime.datetime.now().strftime('%Y-%m-%d_%Hh%Mm')
        csv_name = os.path.join(directory_name, '「{}」[{}].csv'.format(novel_title, today))

        # 列名（1行目）を作成
        col_name = ['No', 'title', 'url', 'date', 'text']

        with open(csv_name, 'w', newline='', encoding='utf-8') as output_csv:
            csv_writer = csv.writer(output_csv)
            csv_writer.writerow(col_name) # 列名を記入

            # csvに1行ずつ書き込み
            for story in stories:
                row_items = [story['No'], story['title'], story['url'], story['date'], story['text']]
                csv_writer.writerow(row_items)

        print(csv_name, ' saved...')

if __name__ == '__main__':
    NameDAO().main()