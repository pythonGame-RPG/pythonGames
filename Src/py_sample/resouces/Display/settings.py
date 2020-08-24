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

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 24

# Game properties
BOOST_POWER = 60
POW_SPAWN_PCT = 20  # 登場する頻度
MOB_FREQ = 5000  # millisecond
CLOUD_FREQ = 15

# LAYER 描かれる順番
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 2
CLOUD_LAYER = 0

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

# スクレイピング除外リスト
DELETE_NAME_LIST = ["%・・%", "%ゴブリン%", "%ァァ%", "%アア%", "%アァ%"]

# 質問メッセージ
Q0001 = '画面の内容で登録しますか？'
Q0002 = '選択したデータを削除しますか？'
Q0003 = '選択したデータを登録しますか？'
# メッセージ
I0001 = '削除が完了しました。'
I0002 = '登録が完了しました。'
# エラーメッセージ
E0001 = '名前とランクが重複しています。'
E0002 = '予期せぬエラーが発生しました。処理を中断します。'
E0003 = 'いずれかのテキストが入力されていません'
E0004 = '中心座標は(0, 0)～({0}, {1})の範囲内で設定してください'