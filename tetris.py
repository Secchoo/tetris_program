from settings import *
import math
from tetromino import Tetromino
import pygame.freetype as ft 


class Text:
    def __init__(self, app):
        self.app = app
        self.font = ft.Font(font_path)

    def get_color(self):
        time = pg.time.get_ticks() * 0.001
        n_sin = lambda t: (math.sin(t) * 0.5 + 0.5) * 255
        return n_sin(time * 0.5), n_sin(time * 0.2), n_sin(time * 0.9)

    def draw(self):
        self.font.render_to(self.app.screen, (win_w * 0.595, win_h * 0.02),
                            text='TETRIS', fgcolor=self.get_color(),
                            size=tile_size * 1.65, bgcolor='black')
        self.font.render_to(self.app.screen, (win_w * 0.65, win_h * 0.22),
                            text='next', fgcolor='orange',
                            size=tile_size * 1.4, bgcolor='black')
        self.font.render_to(self.app.screen, (win_w * 0.64, win_h * 0.67),
                            text='score', fgcolor='orange',
                            size=tile_size * 1.4, bgcolor='black')
        self.font.render_to(self.app.screen, (win_w * 0.64, win_h * 0.8),
                            text=f'{self.app.tetris.score}', fgcolor='white',
                            size=tile_size * 1.8)

class Tetris:
    def __init__(self, app):
        self.app = app
        self.reset()

    def reset(self):
        self.sprite_group = pg.sprite.Group()
        self.get_field_array = self.get_field_array_func()
        self.tetromino = Tetromino(self)
        self.next_tetromino = Tetromino(self, current=False)
        self.speed_up = False

        self.score = 0
        self.full_lines = 0
        self.points_per_lines = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

    def get_score(self):
        self.score += self.points_per_lines[self.full_lines]
        self.full_lines = 0

    def get_field_array_func(self):
        return [[0 for x in range(field_w)] for y in range(field_h)]

    def check_full_lines(self):
        row = field_h - 1
        for y in range(field_h - 1, -1, -1):
            for x in range(field_w):
                self.get_field_array[row][x] = self.get_field_array[y][x]
                if self.get_field_array[y][x]:
                    self.get_field_array[row][x].pos = vec(x, row)
            if sum(map(bool, self.get_field_array[y])) < field_w:
                row -= 1
            else:
                # Only dissolve the full line, and animate blocks upwards
                for x in range(field_w):
                    block = self.get_field_array[row][x]
                    if block:
                        block.alive = False
                        block.sfx_direction = -1  # Animate upwards
                        self.get_field_array[row][x] = 0
                self.full_lines += 1

    def tetromino_blocks_in_array(self):
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.get_field_array[y][x] = block

    def game_over(self):
        # If any block of the new tetromino is in the top row, game over
        if any(block.pos.y < init_pos_offset[1] + 1 for block in self.tetromino.blocks):
            pg.time.wait(300)
            return True
        return False

    def check_tetromino_landing(self):
        if self.tetromino.landing:
            if self.game_over():
                self.reset()
            else:
                self.speed_up = False
                self.tetromino_blocks_in_array()
                self.next_tetromino.current = True
                self.tetromino = self.next_tetromino
                self.next_tetromino = Tetromino(self, current=False)

    def control(self, pressed_key):
        if pressed_key == pg.K_LEFT:
            self.tetromino.move(direction='left')
        elif pressed_key == pg.K_RIGHT:
            self.tetromino.move(direction='right')
        elif pressed_key == pg.K_UP:
            self.tetromino.rotate()
        elif pressed_key == pg.K_DOWN:
            self.speed_up = True

    def grid(self):
        for x in range(field_w):
            for y in range(field_h):
                pg.draw.rect(self.app.screen, 'black',
                             (x * tile_size, y * tile_size, tile_size, tile_size), 1)

    def update(self):
        trigger = [self.app.anim_trigger, self.app.fast_anim_trigger][self.speed_up]
        if trigger:
            self.check_full_lines()
            self.tetromino.update()
            self.check_tetromino_landing()
            self.get_score()
        self.sprite_group.update()

    def draw(self):
        self.grid()
        self.sprite_group.draw(self.app.screen)