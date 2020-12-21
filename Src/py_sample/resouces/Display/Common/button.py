import pygame as pg

# --- class ---

class Button(object):

    def __init__(self, images, position, size):

        # create 3 images
        self._images = images

        # get image size and position
        self._rect = pg.Rect(position, size)
        self.base_font = pg.font.SysFont('Arial', 20, 16)

        # the 'mouse-over' font
        self.mod_font  = pg.font.SysFont('Arial', 20, 16)
        self.mod_font.set_underline(True)

        # select first image
        self._index = 0
        self.cache = {}

    def draw(self, screen):

        # draw selected image
        screen.blit(self._images[self._index], self._rect)

    # これは画面側で制御
    def event_handler(self, event):

        # change selected color if rectange clicked
        if event.type == pg.MOUSEBUTTONDOWN: # is some button clicked
            if event.button == 1: # is left button clicked
                if self._rect.collidepoint(event.pos): # is mouse over button
                    self._index = (self._index+1) % 3 # change image
    
    # 文字のレンダリングキャッシュされる、処理は安価で実施可能
    def render(self, text, mod=False):
        if not mod in self.cache: 
            self.cache[mod] = {}
        if not text in self.cache[mod]: 
            self.cache[mod][text] = (mod_font if self.mod else self.base_font).render(text, True, (255, 255, 255))
        return self.cache[mod][text]
