from .. import utils
from ..button import Button
from ..font import FONTS
from .state import State
import pygame

class Menu(State):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.surf = utils.load_img('data/imgs/test.png')
        self.buttons = {
            'hello': Button(pygame.Rect(30, 30, 80, 20), 'harloo', 'basic')
        }

    def update(self):
        self.handler.canvas.fill((20, 20, 20))
        for key, btn in self.buttons.items():
            btn.update(self.handler.inputs)
            btn.render(self.handler.canvas)
        self.handler.canvas.blit(self.surf, self.handler.inputs['mouse pos'])
        self.handler.canvas.blit(FONTS['basic'].get_surf(f'{round(self.handler.clock.get_fps())} fps'), (0, 0))
