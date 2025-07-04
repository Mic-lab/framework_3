from .. import utils
from ..button import Button
from ..font import FONTS
from .. import animation
from ..entity import Entity, PhysicsEntity
from .state import State
import pygame

class Menu(State):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.surf = animation.Animation.img_db['test']
        self.buttons = {
            'hello': Button(pygame.Rect(30, 30, 80, 20), 'harloo', 'basic')
        }

        self.entity = PhysicsEntity(pos=(30, 30), name='side', action='idle')


    def update(self):
        self.handler.canvas.fill((20, 20, 20))
        for key, btn in self.buttons.items():
            btn.update(self.handler.inputs)
            btn.render(self.handler.canvas)
        self.handler.canvas.blit(self.surf, self.handler.inputs['mouse pos'])

        self.entity.vel[0] = 0
        if self.handler.inputs['held'].get('a'):
            self.entity.vel[0] = -1
            self.entity.animation.flip[0] = True
        elif self.handler.inputs['held'].get('d'):
            self.entity.vel[0] = 1
            self.entity.animation.flip[0] = False
        if self.entity.vel.x == 0:
            self.entity.animation.set_action('idle')
        else:
            self.entity.animation.set_action('run')
        self.entity.update()
        self.entity.render(self.handler.canvas)

        self.handler.canvas.blit(FONTS['basic'].get_surf(f'{round(self.handler.clock.get_fps())} fps'), (0, 0))
