import pygame as pg
from settings import *
import random

vec = pg.math.Vector2

class SpriteSheet:
    def __init__(self, filename):
        """ SpriteSheet専用クラス"""
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        """ spritesheetの中の特定の画像を切り取る """
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width // 2, height // 2))
        return image