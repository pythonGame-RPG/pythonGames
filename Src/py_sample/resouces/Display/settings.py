import csv
import os
import sys
from enum import Enum
from pathlib import Path
import pygame as pg

# game options/settings
TITLE = "WorldSIMU"
LOGIN = "LOGIN"
MES_LOGIN = "ログインIDとパスワードを入力してください。"
WIDTH = 1000
HEIGHT = 600
FPS = 60
FONT_NAME = 'arial'
HS_FILE = "highscore.txt"
SPRITESHEET = "spritesheet_jumper.png"
ROOT_PATH = os.path.dirname(__file__)
sys.path.append(ROOT_PATH + "/CSV")

# Player properties
USER_ID = ""
USER_NAME = ""
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 24
# 反発係数
COEFFICIENT_RESTITUTION = 0.7

# Game properties
BOOST_POWER = 60
POW_SPAWN_PCT = 20  # 登場する頻度
MOB_FREQ = 5000  # millisecond
CLOUD_FREQ = 15

# LAYER 描かれる順番
PLAYER_LAYER = 2
PLAYER_POINT_LAYER = 8
PLATFORM_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 2
CLOUD_LAYER = 0

# ガチャ
GACHA_BALL_LAYER = 2
# 停止後
GACHA_BALL_LAYER2 = 6
GACHA_HONTAI_LAYER = 3
GACHA_KNIGHT_LAYER = 0
GACHA_HAIKEI_LAYER = 1

# PLAY
PLAYER_LAYER = 5
OBJECT_LAYER = 1

# TODO:Starting platformsいらなくなったら削除
PLATFORM_LIST = [(0, HEIGHT - 50),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4),
                 (125, HEIGHT - 350),
                 (350, 200),    
                 (175, 100)]

# define colors
WHITE = (255, 255, 255)
PINK = (255,192,203)
BLACK = (47, 53, 66)
DARKGREY = (27, 140, 141)
LIGHTGREY = (189, 195, 199)
GREEN = (60, 186, 84)
RED = (219, 50, 54)
YELLOW = (244, 194, 13)
BLUE = (72, 133, 237)
LIGHTBLUE = (41, 128, 185)
BGCOLOR = LIGHTBLUE

# sqlデータベース
MST_USERS = "users"
MST_CHARACTERS = "characters"
MST_DANGEON_CHARACTERS = "dangeon_characters"
MST_GENES = "genes"
MST_RACES = "races"
MST_CLASSES = "classes"
MST_TALENTS = "talents"
MST_PERSONALITIES = "personalities"
MST_DANGEONS = "dangeons"
MST_FIELDS = "fields"
MST_LOCATIONS = "locations"
MST_AREAS = "areas"
MST_SPOTS = "spots"
MST_NAMES = "names"

# エラーコード
ERR_MESSAGE1 = "{}は半角英数字で入力してください。"
ERR_MESSAGE2 = "{0}は{1}文字以内で入力してください。"
ERR_MESSAGE3 = "user_idまたはpasswordが間違っています。"
ERR_MESSAGE4 = "パスワードが一致しません"

# 上限下限
LOGIN_MAXNUM = 16
MAX_ERR = 3

# データ起動フラグ
DATA_1 = 1
DATA_2 = 2
DATA_3 = 3

# ランダム色
colorsCollection=['green yellow','yellow','orange','pink','medium purple','cyan','aquamarine']

# スクレイピング除外リスト
DELETE_NAME_LIST = ["%・・%", "%ゴブリン%", "%ァァ%", "%アア%", "%アァ%"]

# 質問メッセージ
Q0001 = '画面の内容で登録しますか？'
Q0002 = '選択したデータを削除しますか？'
Q0003 = '選択したデータを登録しますか？'
Q0004 = '選択した範囲を王国に登録しますか？'
Q0005 = '既存の王国と重複しています。上書きしますか？'
# メッセージ
I0001 = '削除が完了しました。'
I0002 = '登録が完了しました。'
# エラーメッセージ
E0001 = '名前とランクが重複しています。'
E0002 = '予期せぬエラーが発生しました。処理を中断します。'
E0003 = 'いずれかのテキストが入力されていません'
E0004 = '中心座標は(0, 0)～({0}, {1})の範囲内で設定してください'

# img置き場
# (path,size,location, hover)
SHOP_IMG = [
    #("img/knight.png", (200, 400), (100, 100),True),
    ("img/120yen.png", (120, 120), (400, 200),True),
    ("img/480yen.png", (120, 120), (600, 200),True),
    ("img/1200yen.png", (120, 120), (800, 200),True),
    ("img/3000yen.png", (120, 120), (400, 400),True),
    ("img/5000yen.png", (120, 120), (600, 400),True),
    ("img/10000yen.png", (120, 120), (800, 400),True),
    ("img/str120.png", (120, 40), (400, 320),True),
    ("img/str480.png", (120, 40), (600, 320),True),
    ("img/str1200.png", (120, 40), (800, 320),True),
    ("img/str3000.png", (120, 40), (400, 520),True),
    ("img/str5000.png", (120, 40), (600, 520),True),
    ("img/str10000.png", (120, 40), (800, 520),True)
]

CH_KAKIN_KNIGHT = [
    ("img/キャラクター/課金騎士/課金騎士.png", (290, 420), (40, 180),True),
    ("img/キャラクター/課金騎士/課金騎士6.png", (290, 420), (40, 180),True),
    ("img/キャラクター/課金騎士/課金騎士7.png", (290, 420), (40, 180),True),
]

IMG_GACHA_HONTAI = [
    ("img/ガチャ関連/img_gacha_hontai.png", (240, 500), (300, 20),True),
    # ("img/ガチャ関連/img-gacha.png", (290, 420), (40, 180),True),
]

IMG_GACHA_HAIKEI = [
    ("img/ガチャ関連/img_gacha_haikei.png", (190, 500), (325, 20),True),
]

# (path,size,location, probabirity)
IMG_GACHA_BALL = [
    ("img/ガチャ関連/gacha_1.png", (50, 50), (390, 360),50),
    ("img/ガチャ関連/gacha_2.png", (50, 50), (390, 360),37),
    ("img/ガチャ関連/gacha_3.png", (50, 50), (390, 360),10),
    ("img/ガチャ関連/gacha_4.png", (50, 50), (390, 360),3),
]

IMG_GACHA_KNIGHT= [
    ("img/ガチャ関連/gacha_knight.png", None, (390, 360),50),
]

BACK_IMG = {
    "SHOP":"img/酒場背景.png",
    "GACHA":"img/ガチャ関連/gacha_haikei.png",
    "PLAY":"img/操作画面/play_haikei.jpg",
}

MOVE_SCREEN = {
    "GACHA":("img/ガチャ関連/smoke_haikei.png",(959,979))
}

PLAYER_ACTION = {
    ("img/操作画面/left_model.png",(68,250),(WIDTH/2, HEIGHT-100),50),
    ("img/操作画面/right_model.png",(68,250),(WIDTH/2, HEIGHT-100),50),
}

# object：Json形式で一括Arrayに収める
# 家などは表示位置を変更したり可能にしたい
HOUSE_SCREEN = {
    ("img/操作画面/house_a.png",(200, 200),(0,300),50),
}

HUKIDASHI_IMG = [
    ("img/吹き出し/吹き出し1.png", 180, (80, 130),True),
    ("img/吹き出し/吹き出し2.png", 180, (80, 130),True),
    ("img/吹き出し/吹き出し3.png", 180, (80, 130),True),
    ("img/吹き出し/吹き出し4.png", 180, (80, 130),True),
    ("img/吹き出し/吹き出し5.png", 180, (80, 130),True),
]

RARELITY = {
    'common':1,
    'rare':2,
    'superRare':3,
    'ultraRare':4,
}