from settings import *
from tetris import Tetris, Text
import sys
import pathlib


class App:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Tetris')
        self.screen = pg.display.set_mode(win_res)
        self.clock = pg.time.Clock()
        self.set_timer()
        self.images = self.load_assets()
        self.tetris = Tetris(self)
        self.text = Text(self)

    def load_assets(self):
        files = [item for item in pathlib.Path(sprite_dir_path).rglob('*.png') if item.is_file()]
        images = [pg.image.load(file).convert_alpha() for file in files]
        images = [pg.transform.scale(image, (tile_size, tile_size)) for image in images]
        return images

    def set_timer(self):
        self.user_event = pg.USEREVENT + 0
        self.fast_user_event = pg.USEREVENT + 1
        self.anim_trigger = False
        self.fast_anim_trigger = False
        pg.time.set_timer(self.user_event, animation_time_interval)
        pg.time.set_timer(self.fast_user_event, fast_anim_time_interval)

    def update(self):
        self.tetris.update()
        self.clock.tick(FPS)

    def draw(self):
        self.screen.fill(color=bg_color)
        self.screen.fill(color=field_color, rect=(0, 0, *field_res))
        self.tetris.draw()
        self.text.draw()
        pg.display.flip()

    def check_events(self):
        self.anim_trigger = False
        self.fast_anim_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self.tetris.control(pressed_key=event.key)
            elif event.type == self.user_event:
                self.anim_trigger = True
            elif event.type == self.fast_user_event:
                self.fast_anim_trigger = True

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    app = App()
    app.run()
