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
import random

class Gacha:
    def __init__(self,filter):
        """ ゲームを初期化 """
        self.running = True
        self.screen = filter
        #画面再描写(フルスクリーン対応)
        # self.screen.blit(self.filter, (0,0))
        #self.buttons = button.Button()

        self.clock = pg.time.Clock()
        self.PG_ID = "GACHA"
        # self.g_ball = GachaBalls(self)
        self.platforms = None
        self.playing = False
        self.player = None
        self.score = 0
        self.all_sprites = None
        self.knight_flg = True
        self.player_name = []
        self.dir = None
        self.spritesheet = None
        self.jump_sound = None
        self.snd_dir = None
        self.focus_rect = pg.Surface((120,160))
        self.focus_rect.set_colorkey((255, 255, 255))
        self.focus_rect.set_alpha(50)
        # 騎士イベント用
        self.hover = False
        self.select_ball = []
        self.ball_frame = []
        self.gacha_hontai_frame = self.load_images(IMG_GACHA_HONTAI)
        self.gacha_haikei_frame = self.load_images(IMG_GACHA_HAIKEI)
        self.gacha_ball_frame = self.load_images(IMG_GACHA_BALL)
        self.gacha_knight_frame = self.load_images(IMG_GACHA_KNIGHT)
        # NewGameフラグ
        self.rebase = True
        self.font_name = pg.font.match_font(FONT_NAME)  # FONTを探す
        self.character_data = None
        # キャラクタ取得キー
        self.user_id = None
        self.load_key = None
        self.pointer_length = 0
        self.pointer = 0
        self.last_update = 0
        # 金塊画像
        # ファイル名を添え字とした辞書を作成
        self.back_img = pg.image.load(BACK_IMG[self.PG_ID]).convert_alpha()
        self.back_img = pg.transform.scale(self.back_img, (WIDTH,HEIGHT))
        self.smoke_img = pg.image.load(MOVE_SCREEN[self.PG_ID][0]).convert_alpha()
        self.smoke_img = pg.transform.scale(self.back_img,MOVE_SCREEN[self.PG_ID][1])

        # 画面ロード
        self.new()
        self.run()
    
    # 画像読み込み
    def load_images(self,data):
        
        image_list = []
        # TODO:本体が表示されない
        for (str_img, size, location, hover) in data:

            img_name = str_img[str_img.rfind('/')+1:str_img.rfind('.')]
            if img_name not in image_list:
                image = pg.image.load(str_img).convert_alpha()
                if size is not None:
                    image = pg.transform.scale(image, size)
                dicImage = {}
                dicImage['name'] = img_name
                dicImage['img'] = image
                dicImage['size'] = size
                dicImage['location'] = location
                # 画像追加
                image_list.append(dicImage)
                # dicImage['hover_flg'] = hover
            # 表示は一括なのでカット
            # self.screen.blit(dicImage['img'], location)
        return image_list
    
    def load_data(self,image):
        
        # 固定描画（spriteでないもの）
        # rect = img.get_rect()
        self.screen.blit(image['img'], image['location'])
        # TODO:self.rectを作るかどうかは別


    def new(self):
        # ゲームオーバー後のニューゲーム
        self.score = 0
        self.all_sprites = pg.sprite.LayeredUpdates()  # sprite が描かれる順番を指定できるようになる
        self.gacha_hontai = pg.sprite.Group()
        self.gacha_haikei = pg.sprite.Group()
        # TODO:複数個
        self.gacha_ball = pg.sprite.Group()
        self.gacha_knight = pg.sprite.Group()
        # mob を作成した時間を記録
        self.mob_timer = 0
        # 固定オブジェクト表示
        FixedObject(self, self.gacha_haikei_frame,GACHA_HAIKEI_LAYER)
        FixedObject(self, self.gacha_hontai_frame,GACHA_HONTAI_LAYER)

    def update(self):
        # アップデート
        self.all_sprites.update()

        # gacha を作成
        now = pg.time.get_ticks()
        if now - self.mob_timer > 5000 + random.choice(
                [-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            GachaBall(self)
            # 横切る女騎士
            if self.knight_flg == True:
                GachaKnight(self)
                self.knight_flg = False

    def run(self):
        # ゲームループ
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        # pg.mixer.music.fadeout(500)
    
    def events(self):
        # イベント
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYUP:
                # ジャンプを調整 ボタンを押す長さ
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

    # 描画
    def draw(self):

        # ①背景描画→表示順考慮のためSprite化
        self.screen.blit(self.back_img, (0,0))
        # self.load_data(self.gacha_haikei_frame[0])
        # ②玉描画
        self.all_sprites.draw(self.screen)
        # ③ガチャ描画→表示順考慮のためSprite化
        # self.load_data(self.gacha_hontai_frame[0])
        # self.screen.blit(self.player.image, self.player.rect)
        # self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()

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
        
class FixedObject(pg.sprite.Sprite):
    def __init__(self, game, image, layer):
        self._layer = layer
        self.groups = game.all_sprites, game.gacha_knight
        super().__init__(self.groups)
        self.game = game
        self.image = image[0]['img']
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)

class GachaKnight(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = GACHA_KNIGHT_LAYER
        self.groups = game.all_sprites, game.gacha_knight
        super().__init__(self.groups)
        self.game = game
        self.image_up = self.game.gacha_knight_frame[0]['img']
        self.image_down = self.game.gacha_knight_frame[0]['img']
        self.image = self.image_up
        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice([-100, WIDTH + 100])
        self.vx = random.randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        self.rect.centery = HEIGHT
        self.vy = 0
        self.dy = 0.5

    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1
        center = self.rect.center
        if self.dy < 0:
            self.image = self.image_up
        else:
            self.image = self.image_down
        # 衝突判定用のマスク
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.rect.y += self.vy

        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()
            self.game.knight_flg = True

# ガチャ玉単一
class GachaBall(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = GACHA_BALL_LAYER
        self.groups = game.all_sprites, game.gacha_ball
        super().__init__(self.groups)
        self.game = game
        self.screen = game.screen
        self.last_update = 0
        self.current_ball = 0
        self.play_num = 0
        self.running = True
        self.stop_flg = True
        self.name = ''
        self.img = pg.Surface((10, 10))
        self.image = self.randomSelect()
        self.rect = self.image.get_rect()
        self.size = (40,40)
        # self.rect.center = (390,300)
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        # self.eng = (HEIGHT - self.rect.centery)*PLAYER_ACC + 1/2 * (self.vel.y) ** 2
        #self.pos = vec(0, 0)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        # self.update()
    
    def randomSelect(self):
        num_v = random.randint(1,100)
        if num_v <= 3:
            image = self.game.gacha_ball_frame[3]['img']
        elif num_v <= 20:
            image = self.game.gacha_ball_frame[2]['img']
        elif num_v <= 50:
            image = self.game.gacha_ball_frame[1]['img']
        else:
            image = self.game.gacha_ball_frame[0]['img']
        return image

    def update(self):

        now = pg.time.get_ticks()  # 現在のtick(時間)を取得
        # self.animate(now)

        # if now - self.last_update > 5000:
        #     self.last_update = now
        if self.running:
            self.acc = vec(0, PLAYER_GRAV)
            self.running = False

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # TODO:ふわふわ処理
        
        # 摩擦を計算
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # Velocity に Accelerationを足す
        self.vel += self.acc

        # 微かな動きを止める
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        
        if abs(self.vel.y) < 0.1:
            self.vel.y = 0
            self.acc.y = 0


        # Position に Velocity を足す
        self.pos += self.vel + 0.5 * self.acc

        # Check Edges
        
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2
        if self.pos.y >= HEIGHT * 13 / 16 and now - self.last_update > 5000:
            self.vel.y = - COEFFICIENT_RESTITUTION*self.vel.y # self.vel.y / 4
            if self.stop_flg:
                self.stop_flg = False

        # 現在の位置に Positionを設定
        self.rect.midbottom = self.pos

        # 画面からフェードアウトした場合削除
        if self.rect.bottom > HEIGHT + 100 or self.rect.bottom < -100:
            self.kill()

    # ボールが転がって止まるアニメーション    
    def animate(self,now):
        """アニメーション"""
        # now = pg.time.get_ticks()  # 現在のtick(時間)を取得

        # 吹き出しを表示する
        # if self.game.hover:
        if now - self.last_update > 200:
            
            self.last_update = now
            # self.rect.center = center
            
            # self.image = self.walk_frames_l[self.current_frame]
            # self.rect = self.image.get_rect()
            # self.rect.bottom = bottom
        # 衝突判定用のマスク
        self.mask = pg.mask.from_surface(self.image)

pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(TITLE)

Gacha(screen)