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
import numpy as np

class Play:
    def __init__(self,filter):
        """ ゲームを初期化 """
        self.running = True
        self.screen = filter
        #画面再描写(フルスクリーン対応)
        # self.screen.blit(self.filter, (0,0))
        #self.buttons = button.Button()

        self.clock = pg.time.Clock()
        self.PG_ID = "PLAY"
        self.platforms = None
        self.playing = False
        self.object = None
        self.player = None
        # object
        self.obj_player = None

        self.house_rect_list = []
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
        self.player_frame = self.load_images(PLAYER_ACTION)
        # objhouse_listはたたき台
        self.house_list = self.load_images(HOUSE_SCREEN)
        # house表示用
        self.house_frame = self.new_obj_house(self.house_list)
        # 霧(単一)
        self.fog_frame = self.load_images([MOVE_SCREEN[self.PG_ID]])[0]
        self.fog_frame['layer'] = FOG_LAYER
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
        #platoform用
        self.platform_img = pg.image.load(PLATFORM_OBJECT[self.PG_ID]).convert_alpha()
        self.platform_img = pg.transform.scale(self.platform_img, (WIDTH,HEIGHT))

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
        self.player = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.object =  pg.sprite.Group()
        self.fixed_object = pg.sprite.Group()
        self.fog = pg.sprite.Group()
        # TODO:複数個
        # self.gacha_ball = pg.sprite.Group()
        # self.gacha_knight = pg.sprite.Group()
        # mob を作成した時間を記録
        self.mob_timer = 0
        # 固定オブジェクト表示
        self.obj_player = Player(self)
        self.obj_platform = Platform(self)
        # 家
        for data in self.house_frame:
            # 家を表示
            self.house_rect_list.append(FixedObject(self, data))
        
        # 霧
        self.obj_fog = FixedObject(self, self.fog_frame)
    
    # 家を表示する
    def new_obj_house(self,images):

        new_house_images = []
        size_L = 550
        size_M = 250
        size_S = 120
        x_M = 225
        x_S = 360
        rate_L = 9/16
        rate_M = 2/3
        rate_S = 11/16
        house_data = [
            {"location":(0,HEIGHT*rate_L),"size":(size_L,size_L),"layer":4},
            {"location":(WIDTH,HEIGHT*rate_L),"size":(size_L,size_L),"layer":4},
            {"location":(x_M,HEIGHT*rate_M),"size":(size_M,size_M),"layer":3},
            {"location":(WIDTH - x_M,HEIGHT*rate_M),"size":(size_M,size_M),"layer":3},
            {"location":(x_S,HEIGHT*rate_S),"size":(size_S,size_S),"layer":2},
            {"location":(WIDTH - x_S,HEIGHT*rate_S),"size":(size_S,size_S),"layer":2},
        ]
        # new_image作成
        for data in house_data:
            for i_data in images:
                new_house = {}
                new_house['name'] = i_data['name']
                new_house['img'] = i_data['img']
                new_house['location'] = data['location']
                new_house['size'] = data['size']
                new_house['layer'] = data['layer']

                new_house_images.append(new_house)
        
        return new_house_images

    def update(self):
        # アップデート
        self.all_sprites.update()
        # 当たり判定
        self.hitJudge()

        # gacha を作成
        """
        now = pg.time.get_ticks()
        if now - self.mob_timer > 5000 + random.choice(
                [-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            GachaBall(self)
            # 横切る女騎士
            if self.knight_flg == True:
                GachaKnight(self)
                self.knight_flg = False
        """

    # 当たり判定
    def hitJudge(self):

        now = pg.time.get_ticks()  # 現在のtick(時間)を取得
        
        """
        # 【Director】当たり判定処理
        for data in self.house_rect_list:
            # 最低点が被った場合は停止
            if self.obj_player.rect.clip(data.rect).bottom == self.obj_player.rect.bottom:
                # 疑似Rectをセット
                self.obj_player.stop_flg = True
                self.obj_player.stop_pos = self.obj_player.pos
                break

            else:
                self.obj_player.stop_flg = False
                self.obj_player.pos = self.obj_player.stop_pos
                # print(self.obj_player.stop_pos)

        if self.obj_player.stop_flg:
            self.obj_player.pos = self.obj_player.stop_pos

        # dump処理→もっと詳細を表示したい
        if now - self.last_update > 1000:
            self.last_update = now
            print('★'.join([str(self.obj_player.pos),str(self.obj_player.rect.midbottom)]))
        """

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
    def __init__(self, game, image):
        self._layer = image['layer']
        self.groups = game.all_sprites, game.fixed_object
        super().__init__(self.groups)
        # 各属性フラグ
        self.fog_flg = False
        self.name = image['name']
        self.last_update = 0
        self.game = game
        self.location = image['location']
        self.image = image['img']
        self.image = pg.transform.scale(self.image, image['size'])
        self.rect = self.image.get_rect()
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
    
    # update
    def update(self):

        # 霧の発生
        if self._layer == FOG_LAYER:
            self.updateFog()
            self.mask = pg.mask.from_surface(self.image)
        
        if self._layer == 2 or self._layer == 3 or self._layer == 4:
            self.updateHouse()

    def updateHouse(self):
        self.rect.center = self.location

    # 霧
    def updateFog(self):
        
        now = pg.time.get_ticks()  # 現在のtick(時間)を取得

        self.fog_flg = True
        self.vel.x = 0.2
        self.pos.x = self.pos.x + self.vel.x
        self.rect.center = self.pos

        # 歩くアニメーション
        if now - self.last_update > 2000:
            self.last_update = now
            pass

class Platform(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.platforms
        super().__init__(self.groups)
        self.game = game
        # spritesheetから地面の画像を２つ取得
        self.image = self.game.platform_img  # 2つのうち１つをランダムに取得
        self.image.set_colorkey((0, 0, 0))  # 背景を消す
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        # if random.randrange(100) < POW_SPAWN_PCT:
        #     Pow(self.game, self)

# プレイヤーオブジェクト
class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites, game.player
        super().__init__(self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.stop_flg = False
        self.standing_frames = []
        # self.walk_frames_r = []
        # self.walk_frames_l = []
        # self.jump_frame = []
        self.current_frame = 0 # to keep track of animation frame
        self.last_update = 0  # to keep time of animation
        self.last_stop = 0  # to keep time of animation
        self.player_frame = self.game.player_frame
        self.image = self.player_frame[0]['img']
        self.rect = self.image.get_rect()
        self.rect.center = (500, HEIGHT - 100)
        self.pos = vec(self.player_frame[0]['location'])
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.stop_pos = vec(0,0)
        self.before_stop_pos = vec(0,0)

    def jump(self):
        # jump only if on a platform
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2
        if hits and not self.jumping:
            # self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP

    def update(self):

        # 当たり判定
        # for data in self.game.platforms:
        now = pg.time.get_ticks() 
        hits = pg.sprite.spritecollide(self,self.game.platforms,False, pg.sprite.collide_mask)
        # 当たり判定
        if not hits:
            self.stop_flg = False
        else:
            # 本来ならここで衝突したスプライトを精査する
            self.stop_flg = True
            # 停止位置を記録
            self.stop_pos = vec(self.pos.x,self.pos.y)
        
        self.animate()
        # 重力の設定
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        # 上下移動はPlatformと接している問のみ可能
        # 接してからの処理、徐々に加速度を弱めていくのが良いのでは？
        if self.stop_flg:
            if keys[pg.K_UP]:
                self.acc.y = -PLAYER_ACC
            if keys[pg.K_DOWN]:
                self.acc.y = PLAYER_ACC

        # 摩擦を計算
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # Velocity に Accelerationを足す
        self.vel += self.acc

        # 微かな動きを止める
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0

        # Check Edges
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2

        # if self.stop_flg:
        # 速度０処理
        if abs(self.vel.y) < 0.1:
            self.vel.y = 0
            self.acc.y = 0
            # self.stop_flg = True
            # レイヤー順を修正
            # self.game.all_sprites.change_layer(self, GACHA_BALL_LAYER2)
            # self._layer = GACHA_BALL_LAYER2

        # 速度が０になったらホップしてくる処理
        if self.vel.y == 0 and not self.stop_flg:
            self.vel = vec(random.randrange(-10,10), 10)
            
        # ストップ前の判定をスルー
        # バウンド処理  
        if self.pos.y >= HEIGHT * 29 / 32: #and now - self.last_update > 5000:
            self.vel.y = - COEFFICIENT_RESTITUTION*self.vel.y 
            self.pos.y = HEIGHT * 29 / 32
        
        self.pos += self.vel + 0.5 * self.acc

        # 停止時
        if not self.stop_flg:
            # self.posを差し戻し
            self.pos = vec(self.stop_pos.x,self.stop_pos.y)
        # Position に Velocity を足す
        self.rect.midbottom = self.pos

    def animate(self):
        """アニメーション"""
        now = pg.time.get_ticks()  # 現在のtick(時間)を取得
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        # 歩くアニメーション
        if self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(
                    self.player_frame)  # フレーム画像の配列番号を計算
                bottom = self.rect.bottom
                """左右切り替え
                if self.vel.x > 0:
                    self.image = self.player_frame[self.current_frame]
                else:
                    self.image = self.player_frame[self.current_frame]
                """
                self.image = self.player_frame[self.current_frame]['img']
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # アイドルアニメーション
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:  # 現在と最後にupdateした時間を比較
                self.last_update = now  # もしそうだったらlast_updateをnow(現在)に設定
                self.current_frame = (self.current_frame + 1) % len(self.player_frame)  # フレーム画像の配列番号を計算
                bottom = self.rect.bottom  # フレームごとにimageのサイズが変更になるかもしれないから
                # 地面に必ず足がついているように画像が変更になる前のbottom を取得
                self.image = self.player_frame[self.current_frame]['img']  # imageを計算したフレームに画像に変更
                self.rect = self.image.get_rect()  # rectを新たに取得
                self.rect.bottom = bottom  # rectのbottomを更新

        # 衝突判定用のマスク
        self.mask = pg.mask.from_surface(self.image)

# オブジェクト
class Object(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_POINT_LAYER
        self.groups = game.all_sprites, game.object
        super().__init__(self.groups)
        self.game = game
        self.screen = game.screen
        self.last_update = 0
        self.current_ball = 0
        self.play_num = 0
        self.running = True
        self.stop_flg = True
        self.name = ''
        self.image = pg.Surface((10, 10))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2,HEIGHT/2)
    
    def update(self):
        if self.rect.bottom > HEIGHT + 100 or self.rect.bottom < -100:
            self.kill()
    
    def drawCircle(self):
        self.rect = pg.draw.circle(self.image, 'red', self.rect.center,40)

    def getLocation(self,location):
        self.rect.center = location

# ガチャ玉単一
class Enemy(pg.sprite.Sprite):
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
        # 拡大表示用
        self.disp_image = None
        self.validate = True
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

        # Position に Velocity を足す
        self.pos += self.vel + 0.5 * self.acc

        # Check Edges
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2

        if self.stop_flg:
            # 速度０処理
            if abs(self.vel.y) < 0.1:
                self.vel.y = 0
                self.acc.y = 0
                self.stop_flg = False
                # self._layer = GACHA_BALL_LAYER2

            # 速度が０になったらホップしてくる処理
            if self.vel.y == 0:
                self.vel = vec(random.randrange(-10,10), 10)
                
                # ストップ前の判定をスルー
            # バウンド処理  
            if self.pos.y >= HEIGHT * 27 / 32: #and now - self.last_update > 5000:
                self.vel.y = - COEFFICIENT_RESTITUTION*self.vel.y # self.vel.y / 4

        else:
            # 一度のみの処理になってしまう？
            # 拡大再描画
            # self.size = tuple(np.array(np.multiply(self.size,1.05),dtype=int))
            self.rect = self.image.get_rect()
            if self.validate == True:
                print(self.rect)
                self.validate = False

        # 現在の位置に Positionを設定
        self.rect.midbottom = self.pos

        # 画面からフェードアウトした場合削除
        if self.rect.bottom > HEIGHT + 100 or self.rect.bottom < -100:
            self.kill()

    # update内処理動き詳細
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

Play(screen)