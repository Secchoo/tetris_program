from settings import *
import math
from tetromino import Tetromino

class Tetris:
    def __init__(self, app):
        self.app = app
        self.sprite_group = pg.sprite.Group()
        self.get_field_array = self.get_field_array()
        self.tetromino = Tetromino(self)

    def tetromino_blocks_in_array(self):
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.get_field_array[y][x] = block

    def get_field_array(self):
        return[[0 for x in range (field_w)] for y in range(field_h)]

    def check_tetromino_landing(self):
        if self.tetromino.landing:
            self.tetromino_blocks_in_array()
            self.tetromino = Tetromino(self)

    def control(self, pressed_key):
        if pressed_key == pg.K_LEFT:
            self.tetromino.move(direction='left')
        elif pressed_key == pg.K_RIGHT:
            self.tetromino.move(direction='right')

    def grid(self):
        for x in range(field_w):
            for y in range(field_h):
                pg.draw.rect(self.app.screen, 'black',
                             (x * tile_size, y * tile_size, tile_size, tile_size), 1)

    def update(self):
        if self.app.anim_trigger:
            self.tetromino.update()
            self.check_tetromino_landing()
        self.sprite_group.update()

    def draw(self):
        self.grid()
        self.sprite_group.draw(self.app.screen)