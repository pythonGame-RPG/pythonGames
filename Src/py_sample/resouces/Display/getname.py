from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False
import os
import re
import time
import datetime
import csv
import random
from urllib.request import urlopen
# import requests
from bs4 import BeautifulSoup

def main():
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
    #    ,
    #    "https://ncode.syosetu.com/n2267be/" # Ｒｅ：ゼロから始める異世界生活
    #    ,
    #    "https://ncode.syosetu.com/n6316bn/" # 転生したらスライムだった件
    #     ,
    #     "https://ncode.syosetu.com/n2031cu/" # 異世界転移で女神様から祝福を！　～いえ、手持ちの異能があるので結構です～
    #     ,
    #     "https://ncode.syosetu.com/n3009bk/" # 盾の勇者の成り上がり
    #     ,
    #     "https://ncode.syosetu.com/n6475db/" # 私、能力は平均値でって言ったよね！
    #     ,
    #     "https://ncode.syosetu.com/n5881cl/" # 賢者の孫
               ]
    # --------------------------------------
    # ランキングから開始
    stories = []
    name_list = []
    url = random.choice(url_list)
    bs_obj = make_bs_obj(url)
    time.sleep(3)

    # TODO：ranking_listとどちらが早いかを検証する
    #url_list = ["https://ncode.syosetu.com" + a_bs_obj.find("a").attrs["href"] for a_bs_obj in bs_obj.findAll("div", {"class": "rank_h"})]
    #url_list = [a_bs_obj.find("a").attrs["href"] for a_bs_obj in bs_obj.findAll("div", {"class": "rank_h"})]
    # date_list = bs_obj.findAll("dt",{"class":"long_update"})
    # novel_title = bs_obj.find("p",{"class":"novel_title"}).get_text()
    #for s in r'\/*?"<>:|':
    #    novel_title = novel_title.replace(s, '')

    # 各話の本文情報を取得

    # 小説を取得
    novel_list = [a_bs_obj.find("a").attrs["href"] for a_bs_obj in bs_obj.findAll("div", {"class": "rank_h"})]
    time.sleep(3)

    rand_num = random.choices(range(len(novel_list)), k=10)
    for i in rand_num:

        url = novel_list[i]
        bs_obj = make_bs_obj(url)
        # ストーリーを取得
        story_list = ["https://ncode.syosetu.com" + a_bs_obj.find("a").attrs["href"] for a_bs_obj in bs_obj.findAll("dd", {"class": "subtitle"})]

        lim_num = 10
        story_num = len(story_list)
        if story_num < 10:
            lim_num = story_num
        rand_num = random.choices(range(len(story_list)), k=lim_num)
    
        for l in rand_num:
            url = story_list[l]
            bs_obj = make_bs_obj(url)
            nov_text = get_main_text(bs_obj)
            """
            stories.append({
                "No": j+1,
                "title": bs_obj.find("p", {"class": "novel_subtitle"}).get_text(),
                "url": url,
                "date": date_list[j].get_text(),
                "text": get_main_text(bs_obj),
                })
            """
            story_name = re.findall('[\u30A1-\u30FF]{2,10}',nov_text
            name_list.append(story_name)

            print(story_name)

    insert_name(name_list)
    #save_as_csv(stories, novel_title)

def make_bs_obj(url):
    """
    BeautifulSoupObjectを作成
    """
    html = urlopen(url)
    # html = requests.get(url)
    # content_type_encoding = html.encoding if html.encoding != 'ISO-8859-1' else None
    logger.debug('access {} ...'.format(url))

    # return BeautifulSoup(html,"html.parser",from_encoding=content_type_encoding)
    return BeautifulSoup(html,"html.parser")

def get_main_text(bs_obj):
    """
    各話のコンテンツをスクレイピング
    """
    text = ""
    text_htmls = bs_obj.findAll("div",{"id":"novel_honbun"})[0].findAll("p")

    for text_html in text_htmls:
        text = text + text_html.get_text() + "\n\n"
    
    

    return text

def save_as_csv(stories, novel_title = ""):
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
    main()