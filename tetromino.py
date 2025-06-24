from settings import *
import random


class Block(pg.sprite.Sprite):
    def __init__(self, tetromino, pos):
        self.tetromino = tetromino
        self.pos = vec(pos) + init_pos_offset
        self.next_pos = vec(pos) + next_pos_offset
        self.alive = True

        super().__init__(self.tetromino.tetris.sprite_group)
        self.image = tetromino.image
        self.rect = self.image.get_rect()

        self.sfx_image = self.image.copy()
        self.sfx_image.set_alpha(110)
        self.sfx_speed = random.uniform(0.2, 0.6)
        self.sfx_cycles = random.randrange(6, 8)
        self.cycle_count = 0
        self.sfx_direction = 1  # 1 for down, -1 for up (default down)

    def sfx_end_time(self):
        if self.tetromino.tetris.app.anim_trigger:
            self.cycle_count += 1
            if self.cycle_count > self.sfx_cycles:
                self.cycle_count = 0
                return True

    def sfx_run(self):
        self.image = self.sfx_image
        self.pos.y += self.sfx_speed * self.sfx_direction  # Animate in the set direction
        self.image = pg.transform.rotate(self.image, pg.time.get_ticks() * self.sfx_speed)

    def is_alive(self):
        if not self.alive:
            if not self.sfx_end_time():
                self.sfx_run()
            else:
                self.kill()

    def rotate(self, pivot_pos):
        translated = self.pos - pivot_pos
        rotated = translated.rotate(90)
        return rotated + pivot_pos
    
    def set_rect_pos(self):
        pos = [self.next_pos, self.pos][self.tetromino.current]
        self.rect.topleft = pos * tile_size

    def update(self):
        self.is_alive()
        self.set_rect_pos()

    def is_collide(self, pos):
        x, y = int(pos.x), int(pos.y)
        if 0 <= x < field_w and 0 <= y < field_h and (
            y < 0 or not self.tetromino.tetris.get_field_array[y][x]):
            return False
        return True


class Tetromino:
    def __init__(self, tetris, current=True):
        self.tetris = tetris
        self.shape = random.choice(list(tetrominoes.keys()))
        self.image =  random.choice(tetris.app.images)
        self.blocks = [Block(self, pos) for pos in tetrominoes[self.shape]]
        self.landing = False
        self.current = current

    def rotate(self):
        pivot_pos = self.blocks[0].pos
        new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]

        if not self.is_collide(new_block_positions):
            for i, block in enumerate(self.blocks):
                block.pos = new_block_positions[i]

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
