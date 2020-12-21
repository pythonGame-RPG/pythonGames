import pygame as pg
import random
from settings import *
from sprites import *
from login import *
from menu import *
from Sql import *
from os import path
import DTO.characters as DTO
import DAO.charactersDAO as DAO
import tkinter as tk
from datetime import *
import pygame_menu
from pygame.locals import *
import sys
from Common import button

class Shop:
    def __init__(self,filter):
        """ ゲームを初期化 """
        self.running = True
        self.screen = filter
        #画面再描写(フルスクリーン対応)
        # self.screen.blit(self.filter, (0,0))
        #self.buttons = button.Button()

        self.clock = pg.time.Clock()
        self.PG_ID = "SHOP"
        self.all_sprites = pg.sprite.LayeredUpdates() 
        self.platforms = None
        self.playing = False
        self.player = None
        self.score = 0
        self.player_name = []
        self.dir = None
        self.spritesheet = None
        self.jump_sound = None
        self.snd_dir = None
        self.focus_rect = pg.Surface((120,160))
        self.focus_rect.set_colorkey((255, 255, 255))
        self.focus_rect.set_alpha(50)
        # 騎士イベント用
        self.k_data = KakinKnight(self)
        self.h_data = Hukidashi(self)
        self.hover = False
        # NewGameフラグ
        self.rebase = True
        self.font_name = pg.font.match_font(FONT_NAME)  # FONTを探す
        self.character_data = None
        # キャラクタ取得キー
        self.user_id = None
        self.load_key = None
        self.pointer_length = 0
        self.pointer = 0

        # 金塊画像
        # ファイル名を添え字とした辞書を作成
        self.back_img = pg.image.load(BACK_IMG[self.PG_ID]).convert_alpha()
        self.image = {}
        self.hukidashi_image = {}

        # 画面ロード
        self.wait_for_key()

    # ロード
    def load_data(self):
        
        # ボタン描画
        for (str_img, size, location, hover) in SHOP_IMG:

            img_name = str_img[str_img.rfind('/')+1:str_img.rfind('.')]
            if img_name not in self.image:
                image = pg.image.load(str_img).convert_alpha()
                image = pg.transform.scale(image, size)
                self.image[img_name] = {}
                self.image[img_name]['img'] = image
                self.image[img_name]['size'] = size
                self.image[img_name]['location'] = location
                # self.image['hover_flg'] = hover
            self.screen.blit(self.image[img_name]['img'], location)

    # 画面構成
    def create_display(self):
        # キー待ち
        self.wait_for_key()
    
    def draw_display(self):
        pass
    
    def show_start_screen(self, user_data):
        # ゲームスタート画面
        # character_idにusersのFKをセット
        self.user_id = user_data[0]['user_id']
        # 取得SQLを作成
        self._characterDAO = DAO.CharacterDAO()
        sql = self._characterDAO.select(MST_CHARACTERS)
        sql = self._characterDAO.where(sql, {'user_id': self.user_id})

        # sqlを実行してcharacterデータを取得
        self.character_data = self._characterDAO.execute(sql)
        
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
        # ここでキー押下待ち
        self.wait_for_key()
        # pg.mixer.music.fadeout(500)

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

    # TODO:キー押下待ち
    def wait_for_key(self, running = True):
        waiting = True
        self.running = running
        set_img = None

        while waiting:
            pg.display.update() 
            self.clock.tick(FPS)
            # 課金騎士アニメーション
            self.k_data.animate()
            # 吹き出しアニメーション
            self.h_data.animate()

            for event in pg.event.get():
                keys = pg.key.get_pressed()
                # 背景画像を描画

                self.screen.blit(self.back_img, (0,0))
                
                self.load_data()
                # 座標確認用
                self.draw_text(str(pg.mouse.get_pos()),10,(255,255,255),20,20)
                # バツでゲーム終了
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                # ニューゲームKEYUPはキーを離した状態（不明）

                # ボタン描画
                for dkey, dval in self.image.items():
                    
                    if dval['img'].get_rect(topleft=dval['location']).collidepoint(pg.mouse.get_pos()):

                        location_v = dval['location']

                        # 画像タイトルが別画像であることを考慮してロケーションを再設定
                        if  'str' in dkey:
                            t_list = list(dval['location'])
                            t_list[1] = t_list[1] - 120
                            location_v = tuple(t_list)

                        self.screen.blit(self.focus_rect, location_v)

                        if dkey is not set_img:
                            set_img = dkey
                            hover_key = dkey+' was hovered'
                            print(hover_key)
                        
                        self.hober = True
                    
                    self.hover = False
                
                # キャラクター描画
                """
                for dkey, dval in self.character_image.items():
                    
                    if dval['img'].get_rect(topleft=dval['location']).collidepoint(pg.mouse.get_pos()):

                        location_v = dval['location']

                        # TODO:ホバー処理
                        # self.screen.blit(self.focus_rect, location_v)

                        if dkey is not set_img:
                            set_img = dkey
                            hover_key = dkey+' was hovered'
                            print(hover_key)
                """

                if event.type == pg.KEYUP:
                    # qを押したら処理を抜ける
                    if keys[pg.K_q] | keys[pg.K_ESCAPE]:
                        waiting = False
                        self.rebase = False

                # クリックがあった場合
                if event.type == pg.MOUSEBUTTONDOWN:
                    # calling 'render' over and over again is cheap now, since the resut is cached
                    # 結果がキャッシュされるため、「render」を何度も呼び出すのは今では安価です
                    for text in [dkey for (dkey, dval) in self.image.items() if dval['img'].get_rect().collidepoint(pg.mouse.get_pos())]:
                        print('{} was clicked'.format(text))
                        """
                        app = gui.App()
                        dialog = SimpleDialog()
                        app.init(dialog)
                        """
                        
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
        text_rect.midtop = (int(x), int(y))
        self.screen.blit(text_surface, text_rect)

    # 左詰めテキスト表示
    def draw_left_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midleft = (x, y)
        self.screen.blit(text_surface, text_rect)
        
# 課金騎士
class KakinKnight(pg.sprite.Sprite):
    def __init__(self, game):
        # self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        super().__init__(self.groups)
        self.game = game
        self.screen = game.screen
        self.walking = False
        self.image = {}
        self.kakin_frame = []
        self.load_data()
        self.current_frame = 0  # to keep track of animation frame
        self.last_update = 0  # to keep time of animation
        self.start_image = self.kakin_frame[0][0]
        self.rect = self.start_image.get_rect()
        self.rect.center = (40, HEIGHT - 100)

    def load_data(self):
        # キャラクター描画
        for (str_img, size, location, hover) in CH_KAKIN_KNIGHT:

            img_name = str_img[str_img.rfind('/')+1:str_img.rfind('.')]
            if img_name not in self.image:
                image = pg.image.load(str_img).convert_alpha()
                image = pg.transform.scale(image, size)
                self.image[img_name] = {}
                self.image[img_name]['img'] = image
                self.image[img_name]['size'] = size
                self.image[img_name]['location'] = location
                # self.image['hover_flg'] = hover
            self.screen.blit(self.image[img_name]['img'], location)
        
        self.kakin_frame = [(dval['img'],dval['location']) for (dkey, dval) in self.image.items()]
        
    def animate(self):
        """アニメーション"""
        now = pg.time.get_ticks()  # 現在のtick(時間)を取得

        # 吹き出しを表示する
        # if self.game.hover:
        if now - self.last_update > 200:
            self.last_update = now
            self.status = False
            self.current_frame = (self.current_frame + 1) % len(self.kakin_frame)  # フレーム画像の配列番号を計算
            bottom = self.rect.bottom
            # self.f_image = self.
            
            self.current_image = self.kakin_frame[self.current_frame][0]
            self.current_location = self.kakin_frame[self.current_frame][1]
            self.screen.blit(self.current_image, self.current_location)
            self.rect = self.current_image.get_rect()
            self.rect.bottom = bottom

# 吹き出し（クラス化した方が楽かな）
class Hukidashi(pg.sprite.Sprite):
    def __init__(self, game):
        # self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        super().__init__(self.groups)
        self.game = game
        self.screen = game.screen
        self.walking = False
        self.jumping = False
        self.hukidashi_frame = []
        self.image = {}
        self.load_data()
        self.current_frame = 0  # to keep track of animation frame
        self.last_update = 0  # to keep time of animation
        self.start_image = self.hukidashi_frame[0][0]
        self.rect = self.start_image.get_rect()
        self.rect.center = (40, HEIGHT - 100)

    def load_data(self):
        # キャラクター描画
        for (str_img, size, location, hover) in CH_KAKIN_KNIGHT:

            img_name = str_img[str_img.rfind('/')+1:str_img.rfind('.')]
            if img_name not in self.image:
                image = pg.image.load(str_img).convert_alpha()
                image = pg.transform.scale(image, size)
                self.image[img_name] = {}
                self.image[img_name]['img'] = image
                self.image[img_name]['size'] = size
                self.image[img_name]['location'] = location
                # self.image['hover_flg'] = hover
            self.screen.blit(self.image[img_name]['img'], location)
        
        self.hukidashi_frame = [(dval['img'],dval['location'])  for (dkey, dval) in self.image.items()]
        
    def animate(self):
        """アニメーション"""
        now = pg.time.get_ticks()  # 現在のtick(時間)を取得

        # 吹き出しを表示する
        # if self.game.hover:
        if now - self.last_update < 200:
            self.current_frame = 0  # フレーム画像の配列番号を計算
            bottom = self.rect.bottom
            # self.f_image = self.
            
            self.current_image = self.hukidashi_frame[self.current_frame][0]
            self.current_location = self.hukidashi_frame[self.current_frame][1]
            self.screen.blit(self.current_image, self.current_location)
            self.rect = self.current_image.get_rect()
            self.rect.bottom = bottom
        else:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.hukidashi_frame)  # フレーム画像の配列番号を計算
            bottom = self.rect.bottom
            # self.f_image = self.
            
            self.current_image = self.hukidashi_frame[self.current_frame][0]
            self.current_location = self.hukidashi_frame[self.current_frame][1]
            self.screen.blit(self.current_image, self.current_location)
            self.rect = self.current_image.get_rect()
            self.rect.bottom = bottom

"""
class SimpleDialog(gui.Dialog):
    def __init__(self):
        title = gui.Label("Spam")
        main = gui.Container(width=20, height=20)
        # I patched PGU to use new style classes.
        super(SimpleDialog, self).__init__(title, main, width=40, height=40)

    def close(self, *args, **kwargs):
        print('closing')
        return super(SimpleDialog, self).close(*args, **kwargs)
"""

pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(TITLE)

Shop(screen)