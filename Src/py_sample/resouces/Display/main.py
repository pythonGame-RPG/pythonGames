import pygame as pg
import random
from import_autoloader import *
from settings import *
from sprites import *
from login import *
from menu import *
from Sql import *
from os import path

class Game:
    def __init__(self):
        """ ゲームを初期化 """
        self.running = True
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.all_sprites = None
        self.platforms = None
        self.playing = False
        self.player = None
        self.score = 0
        self.player_name = []
        self.dir = None
        self.spritesheet = None
        self.jump_sound = None
        self.snd_dir = None
        # NewGameフラグ
        self.rebase = True
        self.font_name = pg.font.match_font(FONT_NAME)  # FONTを探す
        self.load_data()
        self.character_data = None
        # キャラクタ取得キー
        self.user_id = None
        self.load_key = None
        self.pointer_length = 0
        self.pointer = 0

    def load_data(self):
        """ Player_nameデータをロード """
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        
        # spritesheetをロード
        self.spritesheet = SpriteSheet(path.join(img_dir, SPRITESHEET))

        # load clouds
        self.cloud_images = []
        for i in range(1, 4):
            self.cloud_images.append(
                pg.image.load(
                    path.join(img_dir, 'cloud{}.png'.format(i))).convert())

    def new(self,load_key):

        self.name = 0
        self.all_sprites = pg.sprite.LayeredUpdates()  # sprite が描かれる順番を指定できるようになる    
        self.powerups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.clouds = pg.sprite.Group()

        self.player = Player(self)

        # mob を作成した時間を記録
        self.mob_timer = 0
    
    def show_start_screen(self, user_data):
        # ゲームスタート画面
        self.character_select_sql = sql_query()
        # character_idにusersのFKをセット
        self.user_id = user_data[0]['user_id']
        # 取得SQLを作成
        sql = self.character_select_sql.select(MST_CHARACTERS)
        sql = self.character_select_sql.where(sql, {'user_id': self.user_id})

        # sqlを実行してcharacterデータを取得
        self.character_data = self.character_select_sql.execute(sql)
        
        # 名前をリストに格納
        for d in self.character_data:
            if d['name'] not in self.player_name:
                self.player_name.append(d['name'])

        """
        pg.mixer.music.load(path.join(self.snd_dir, "Yippee.ogg"))
        pg.mixer.music.play(loops=-1)
        pg.mixer.music.set_volume(0.05)
        """
        # TODO:データ順にプレイヤー名を表示
        self.screen.fill(BGCOLOR)
        self.draw_display()
        # ここでキー押下待ち
        self.wait_for_key()
        # pg.mixer.music.fadeout(500)

    # プレイヤー名を描画
    def draw_display(self):
        # iはフォーカス順
        i = 0
        for name in self.player_name:
            self.draw_left_text("{0}. {1}".format(i + 1,name), 22, self.get_color(i),
                            WIDTH / 4, 15+20*(i + 1))
            self.draw_left_text("Press F{0}Key".format(i + 1), 22, self.get_color(i),
                            5*WIDTH / 8, 15+20*(i + 1))
            i += 1
        # 画面文字列の描画
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrows to move, Space to jump", 22, WHITE, WIDTH / 2,
                       HEIGHT / 2)
        self.draw_text("Press a key to play", 22, self.get_color(i), WIDTH / 2,
                       HEIGHT * 3 / 4)
        self.draw_text("sign up", 22, self.get_color(i+1), WIDTH / 2,
                       HEIGHT * 7 / 8)
        pg.display.flip()

    # ポインターを設定  
    def set_pointer(self, i):
        # player_name(0-2),sign_up
        self.pointer_length = len(self.player_name) + 2
        self.pointer = (self.pointer + i) % self.pointer_length
    
    # 通常時:WHITE、フォーカス時:PINK
    def get_color(self, i):
        if i == self.pointer:
            return PINK
        else:
            return WHITE

    def show_go_screen(self):
        # ゲームオーバー画面
        if not self.running:
            return
        """
        pg.mixer.music.load(path.join(self.snd_dir, "Yippee.ogg"))
        pg.mixer.music.play(loops=-1)
        """
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: {}".format(str(self.score)), 22, WHITE,
                       WIDTH / 2,
                       HEIGHT / 2)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH / 2,
                       HEIGHT * 3 / 4)
        if self.score > 0:
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2,
                           HEIGHT / 2 + 40)
        else:
            self.draw_text("HIGH SCORE: {}".format("See you!"), 22,
                           WHITE,
                           WIDTH / 2, HEIGHT / 2 + 40)
        pg.display.flip()
        self.wait_for_key(False)
        pg.mixer.music.fadeout(500)

    # TODO:キー押下待ち
    def wait_for_key(self, running = True):
        waiting = True
        self.running = running

        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                keys = pg.key.get_pressed()
                # バツでゲーム終了
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                # ニューゲームKEYUPはキーを離した状態（不明）

                if event.type == pg.KEYUP:
                    # qを押したら処理を抜ける
                    if keys[pg.K_q] | keys[pg.K_ESCAPE]:
                        waiting = False
                        self.rebase = False
                        
                # キーイベント
                if event.type == pg.KEYDOWN:
                    # 起動データが存在、かつF★を押したらデータ★を起動
                    if len(self.player_name) == 1 & keys[pg.K_F1]:
                        self.load_key = DATA_1
                    if len(self.player_name) == 2 & keys[pg.K_F2]:
                        self.load_key = DATA_2
                    if len(self.player_name) == 3 & keys[pg.K_F3]:
                        self.load_key = DATA_3 
                    # 上を押下した場合フォーカス上
                    if keys[pg.K_UP]:
                        self.set_pointer(-1)
                        self.draw_display()
                    # 上を押下した場合
                    if keys[pg.K_DOWN]:
                        self.set_pointer(+1)
                        self.draw_display()
                    # Enterを押下した場合
                    if keys[pg.K_RETURN]:
                        # データ起動
                        if self.pointer + 1 <= len(self.player_name):
                            # メニュー呼び出し
                            m = Menu()
                            m.run(self.character_data)
                        self.draw_display()

                # spaceで問答無用に終了
                if keys[pg.K_SPACE]:
                    self.rebase = False

    # 真ん中詰めテキスト表示
    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    # 左詰めテキスト表示
    def draw_left_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midleft = (x, y)
        self.screen.blit(text_surface, text_rect)

# gamestart以降show_start_screen()は実行されない
g = Game()

# ログイン画面を表示
l = Login()
l.mainloop()

# ユーザ―データの有無を確認
if(len(l.user_data) == 0):
    pg.quit

# rebaseフラグ：Falseにならない限りゲームは終了しない。
while g.rebase:
    # メニュー画面に遷移
    g.show_start_screen(l.user_data)

    while g.running:
        # ロードデータの選択チェック
        if g.load_key is not None:
            g.new(g.load_key)
        # ロードデータが選択されなかった場合
        g.show_go_screen()

pg.quit()
