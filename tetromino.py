from settings import *


class Block(pg.sprite.Sprite):
    def __init__(self, tetromino, pos):
        self.tetromino = tetromino

        super().__init__(self.tetromino.tetris.sprite_group)
        self.image = pg.Surface((tile_size, tile_size))
        self.image.fill('green')

        self.rect = self.image.get_rect()
        self.rect.topleft = pos[0] * tile_size, pos[1] * tile_size


class Tetromino:
    def __init__(self, tetris):
        self.tetris = tetris
        Block(self, (4, 7))

    def update(self):
        pass    