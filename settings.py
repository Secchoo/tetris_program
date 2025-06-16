import pygame as pg

vec = pg.math.Vector2

FPS = 60
field_color = (48, 39, 32)
bg_color = (24, 89, 117)

sprite_dir_path = 'assets/sprites'
font_path = 'assets/font/FREAKSOFNATUREMASSIVE.ttf'

animation_time_interval = 150 #milliseconds
fast_anim_time_interval = 15

tile_size = 50
field_size = field_w, field_h = 10, 20
field_res = field_w * tile_size, field_h * tile_size

field_scale_w, field_scale_h = 1.7, 1.0
win_res = win_w, win_h = field_res[0] * field_scale_w, field_res[1] * field_scale_h

