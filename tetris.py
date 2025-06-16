from settings import *
import math

class Tetris:
    def __init__(self, app):
        self.app = app

    def grid(self):
        for x in range(field_w):
            for y in range(field_h):
                pg.draw.rect(self.app.screen, 'black',
                             (x * tile_size, y * tile_size, tile_size, tile_size), 1)

    def update(self):
        pass

    def draw(self):
        self.grid()