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

    def is_collide(self, pos):
        x, y = int(pos.x), int(pos.y)
        if 0 <= x < field_w and 0 <= y < field_h:
            return False
        return True


class Tetromino:
    def __init__(self, tetris):
        self.tetris = tetris
        self.shape = random.choice(list(tetrominoes.keys()))
        self.blocks = [Block(self, pos) for pos in tetrominoes[self.shape]]
        self.landing = False

    def is_collide(self, block_positions):
        return any(block.is_collide(pos) for block, pos in zip(self.blocks, block_positions))

    def move(self, direction):
        move_direction = move_directions[direction]
        new_block_positions = [block.pos + move_direction for block in self.blocks]
        is_collide = self.is_collide(new_block_positions)

        if not is_collide:
            for block in self.blocks:
                block.pos += move_direction
        elif direction == 'down':
            self.landing = True

    def update(self):
        self.move(direction='down')
