# initialize pygame and create window
import pygame as pg
from settings import *
from Sql import *
from validate import *
import random
import tkinter as tk
from turtle import *

# Login classes
class Login:
    def __init__(self):
        """ login画面を初期化 """
        self.running = True
        pg.init()
        pg.mixer.init()
        self.running = True
        self.user_id = None
        self.passwd = None
        self.error = {}
        # 半角英数字エラー
        self.error['digit'] = {}
        # 文字列の長さエラー
        self.error['length'] = {}
        # 辞書型データをvalidateに渡す。
        self.data = {"user_id":self.user_id, "password":self.passwd}
        pg.display.set_caption(LOGIN)
        self.clock = pg.time.Clock()
        self.font_name = pg.font.match_font(FONT_NAME)  # FONTを探す
        self.users = None

    # 入力チェック
    def validate(self, data):
        v = self.validate()
        # 入力値をループ
        for dkey, dvalue in data.items():
            # 半角英数字チェック
            if(v.isdigit(dvalue) == False):
                self.error['digit'].setdefault(dkey, format(ERR_MESSAGE1, dkey))
            # 文字数制限チェック
            if(v.v_length(dvalue, LOGIN_MAXNUM)):
                self.error['length'].setdefault(dkey, format(ERR_MESSAGE2, dkey, LOGIN_MAXNUM))
        
        # エラーの場合エラー文を返す
        if(self.error != None):
            return self.error

        self.user = users()
        self.user.select(MST_USERS, data)
        sql = self.user.select(MST_USERS)
        sql = self.user.where(sql,data)

        # sqlを実行してデータを取得
        user_data = self.user.execute(sql)
        
        # エラーの場合エラー文を返す
        if(user_data == None):
            self.error['length'].setdefault(dkey, format(ERR_MESSAGE2, dkey, LOGIN_MAXNUM))
            return self.error


    def show_start_screen(self):
        # ゲームスタート画面
        # 音楽
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text(MES_LOGIN, 22, WHITE, WIDTH / 2,
                       HEIGHT / 2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2,
                       HEIGHT * 3 / 4)
        """データ順にプレイヤー名を表示"""
        i = 0
        for name in self.player_name:
            i += 1
            self.draw_left_text("{0}. {1}".format(i,name), 22, WHITE,
                            WIDTH / 4, 15+20*i)
            self.draw_left_text("Press F{0}Key".format(i), 22, WHITE,
                            5*WIDTH / 8, 15+20*i)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)
        
"""
# Game Loop
running = True
while running:
    # keep loop running at the right speed
    # Process input (events)

    # update

    # Draw / render

    pg.display.flip()

pg.quit()
"""