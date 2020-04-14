import pygame as pg
import random
from import_autoloader import *
from settings import *
from sprites import *
from login import *
from Sql import *
from os import path

# menuクラス一覧表示
class Menu:
    def __init__(self):
        self.bar = None
    # load sound
    """
    self.snd_dir = path.join(self.dir, 'snd')
    self.jump_sound = pg.mixer.Sound(
        path.join(self.snd_dir, 'Jump33.wav'))
    self.jump_sound.set_volume(0.1)
    self.boost_sound = pg.mixer.Sound(
        path.join(self.snd_dir, 'Boost16.wav'))
    self.boost_sound.set_volume(0.1)
    """
   

# キーイベント

# 画像の描画
"""
    def run(self):
        # ゲームループ
        # 音楽を再生 (-1 はループ)
        pg.mixer.music.play(loops=-1)
        pg.mixer.music.set_volume(0.3)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500) 

    def update(self):
        # アップデート
        self.all_sprites.update()

        # mob を作成
        now = pg.time.get_ticks()
        if now - self.mob_timer > 5000 + random.choice(
                [-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self)

        # hit mobs?
        # pg.sprite.collide_maskでplayerとmobに設定したself.maskを使用して衝突判定
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False,
                                           pg.sprite.collide_mask)
        if mob_hits:
            self.playing = False

        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                # 問題： 2つ同時にspritecollideした場合、飛び移れない
                # 解決: より下にある地面を探す
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit

                # 空中に立っているバグを修正
                if lowest.rect.right + 10 > self.player.pos.x > lowest.rect.left - 10:
                    # 足が次の地面よりも高い位置にある場合のみに飛び移れる
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False

        # もしplayerが画面上部1/4に達したら
        if self.player.rect.top <= HEIGHT / 4:
            # 低い確率でCloudを作成
            if random.randrange(100) < CLOUD_FREQ:
                Cloud(self)

            self.player.pos.y += max(abs(self.player.vel.y), 2)  # abs = 絶対値を取得

            for cloud in self.clouds:
                # 雲は背景だからゆっくり降りていく
                cloud.rect.y += max(abs(self.player.vel.y / 2), 2)

            # mob もplayerの移動とともに下に移動するように
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                # 画面外に行ったplatformを消す
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10

        # もしPOWERUPにあたったら
        pow_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for pow in pow_hits:
            if pow.type == 'boost':
                self.boost_sound.play()
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False

        # ゲームオーバー
        # TODO:落下を表現、いらなくなったら消す
        # playerのspriteが画面の高さ以下になったらplaying = False
        if self.player.rect.bottom > HEIGHT:
            # 全てのspriteが画面上部に消えていく
            # 全てのspriteでループさせる→velはベクトル
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)  # max値を取得
                if sprite.rect.bottom < 0:  # spriteが画面上部に消えたら
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

        # 新しいplatform を作成 / 画面には平均的に同じ数のplatform
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)

            Platform(self, random.randrange(0, WIDTH - width),
                     random.randrange(-75, -30))

    def events(self):
        # イベント
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            # キーを押している間、かつそれがスペースの場合
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

            # キーを離している間、かつそれがスペースの場合    
            if event.type == pg.KEYUP:
                # ジャンプを調整 ボタンを押す長さ
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

    def draw(self):
        # 描画
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        # LAYERのおかげで画面にblitをしなくて良くなる
        # self.screen.blit(self.player.image, self.player.rect)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
    """