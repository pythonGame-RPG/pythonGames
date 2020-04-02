# initialize pygame and create window
import pygame as pg
from settings import *
import random


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
        pg.display.set_caption(LOGIN)
        self.clock = pg.time.Clock()
        self.font_name = pg.font.match_font(FONT_NAME)  # FONTを探す
        self.load_data()

    def load_data(self):
        """ Player_nameデータをロード """
        

# Game Loop
running = True
while running:
    # keep loop running at the right speed
    # Process input (events)

    # update

    # Draw / render

    pg.display.flip()

pg.quit()