from pygame.locals import *
from random import randint
import pygame
import time
import Characters
import Game
import Player
import pyGame_sample1

class App:

    windowWidth = 800
    windowHeight = 600
    player = 0
    characters = 0

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._characters_surf = None
        self.game = Game.Game()
        self.player = Player.Player(3) 
        self.characters = Characters.Characters(5,5)

    # ウィンドウ・画像の設置
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)

        pygame.display.set_caption('Pygame pythonspot.com example')
        self._running = True
        self._image_surf = pygame.image.load("block.jpg").convert()
        self._characters_surf = pygame.image.load("block.jpg").convert()

    # イベントフラグ設置
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    # 勝敗判定
    def on_loop(self):
        self.player.update()

        for i in range(0,self.player.length):
            if self.game.isCollision(self.characters.x,self.characters.y,self.player.x[i], self.player.y[i],44):
                self.characters.x = randint(2,9) * 44
                self.characters.y = randint(2,9) * 44
                self.player.length = self.player.length + 1


        for i in range(2,self.player.length):
            if self.game.isCollision(self.player.x[0],self.player.y[0],self.player.x[i], self.player.y[i],40):
                print("You lose! Collision: ")
                print("x[0] (" + str(self.player.x[0]) + "," + str(self.player.y[0]) + ")")
                print("x[" + str(i) + "] (" + str(self.player.x[i]) + "," + str(self.player.y[i]) + ")")
                exit(0)

        pass

    # 
    def on_render(self):
        self._display_surf.fill((0,0,0))
        # self.player.draw(self._display_surf, self._image_surf)
        # self.characters.draw(self._display_surf, self._characters_surf)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    """
    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while( self._running ):
            pygame.event.pump()
            keys = pygame.key.get_pressed() 

            if (keys[K_RIGHT]):
                self.player.moveRight()

            if (keys[K_LEFT]):
                self.player.moveLeft()

            if (keys[K_UP]):
                self.player.moveUp()

            if (keys[K_DOWN]):
                self.player.moveDown()

            if (keys[K_ESCAPE]):
                self._running = False

            self.on_loop()
            self.on_render()

            time.sleep (50.0 / 1000.0);
        
        self.on_cleanup()
    """

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

            if (keys[K_F1]):
                self.player.moveRight()

            if (keys[K_F2]):
                self.player.moveLeft()

            if (keys[K_F3]):
                self.player.moveUp()

            if (keys[K_F4]):
                self.player.moveDown()
                self.player.moveUp()

            if (keys[K_F5]):
                self.player.moveDown()

            if (keys[K_ESCAPE]):
                self._running = False
                self.player.moveDown()

            if (keys[K_q]):
                self._running = False
                self.player.moveDown()
