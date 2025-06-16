from settings import *
import random


class Block(pg.sprite.Sprite):
    def __init__(self, tetromino, pos):
        self.tetromino = tetromino
        self.pos = vec(pos) + init_pos_offset

        super().__init__(self.tetromino.tetris.sprite_group)
        self.image = pg.Surface((tile_size, tile_size))
        self.image.fill('green')

        self.rect = self.image.get_rect()
    
    def set_rect_pos(self):
        self.rect.topleft = self.pos * tile_size

    def update(self):
        self.set_rect_pos()


class Tetromino:
    def __init__(self, tetris):
        self.tetris = tetris
        self.shape = random.choice(list(tetrominoes.keys()))
        self.blocks = [Block(self, pos) for pos in tetrominoes[self.shape]]

    def move(self, direction):
        move_direction = move_directions[direction]
        for block in self.blocks:
            block.pos += move_direction

    def update(self):
        self.move(direction='down')
        pg.time.wait(200) #simulate a slow falling block    