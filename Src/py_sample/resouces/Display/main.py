import pygame as pg
import random
from import_autoloader import *
from settings import *
from sprites import *
from login import *
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

    def load_data(self):
        """ Player_nameデータをロード """
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        for line in open(path.join(self.dir, HS_FILE), 'r'):
            f = line[:-1].split(',')
            try:
                self.player_name = f
            except:
                self.player_name = 0
        # spritesheetをロード
        self.spritesheet = SpriteSheet(path.join(img_dir, SPRITESHEET))

        # load clouds
        self.cloud_images = []
        for i in range(1, 4):
            self.cloud_images.append(
                pg.image.load(
                    path.join(img_dir, 'cloud{}.png'.format(i))).convert())

        # load sound
        self.snd_dir = path.join(self.dir, 'snd')
        self.jump_sound = pg.mixer.Sound(
            path.join(self.snd_dir, 'Jump33.wav'))
        self.jump_sound.set_volume(0.1)
        self.boost_sound = pg.mixer.Sound(
            path.join(self.snd_dir, 'Boost16.wav'))
        self.boost_sound.set_volume(0.1)

    def new(self):
        # ゲームオーバー後のニューゲーム
        """TODO:既存ロジック
        self.score = 0
        self.all_sprites = pg.sprite.LayeredUpdates()  # sprite が描かれる順番を指定できるようになる
        self.platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.clouds = pg.sprite.Group()

        self.player = Player(self)

        # platform→地面のリスト
        for plat in PLATFORM_LIST:
            Platform(self, *plat)

        # mob を作成した時間を記録
        self.mob_timer = 0

        # 音楽を読み込む
        if self.snd_dir:
            pg.mixer.music.load(path.join(self.snd_dir, "Happy Tune.ogg"))
        for i in range(8):
            c = Cloud(self)
            c.rect.y += 500
        self.run()
        """
        self.name = 0
        self.all_sprites = pg.sprite.LayeredUpdates()  # sprite が描かれる順番を指定できるようになる    
        self.powerups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.clouds = pg.sprite.Group()

        self.player = Player(self)

        # mob を作成した時間を記録
        self.mob_timer = 0

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

    def show_start_screen(self):
        # ゲームスタート画面
        # 音楽
        pg.mixer.music.load(path.join(self.snd_dir, "Yippee.ogg"))
        pg.mixer.music.play(loops=-1)
        pg.mixer.music.set_volume(0.05)
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrows to move, Space to jump", 22, WHITE, WIDTH / 2,
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

    def show_go_screen(self):
        # ゲームオーバー画面
        if not self.running:
            return
        pg.mixer.music.load(path.join(self.snd_dir, "Yippee.ogg"))
        pg.mixer.music.play(loops=-1)
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
        # 
        pg.display.flip()
        self.wait_for_key(False)
        pg.mixer.music.fadeout(500)

    # キー押下待ち
    def wait_for_key(self, running = True):
        waiting = True
        self.running = running

        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                keys = pg.key.get_pressed()
                # ゲーム終了
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                # ニューゲーム
                if event.type == pg.KEYUP:
                    waiting = False
                    if keys[pg.K_q]:
                        self.rebase = False
                # qを押したら処理を抜ける
                if keys[pg.K_SPACE]:
                    self.rebase = False
    
    # F1キーが押された場合の処理
    def procF1key():
        # データ１を起動



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
l = login.Login()
# rebaseフラグ：Falseにならない限りゲームは終了しない。
while g.rebase:
    # ログイン画面に遷移

    g.show_start_screen()

    while g.running:
        g.new()
        g.show_go_screen()

pg.quit()
