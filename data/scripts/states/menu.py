from .. import utils
from ..button import Button
from ..font import FONTS
from .. import animation
from ..entity import Entity, PhysicsEntity
from ..timer import Timer
from .state import State
import pygame

class Menu(State):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.surf = animation.Animation.img_db['test']
        self.buttons = {
            'hello': Button(pygame.Rect(30, 30, 80, 20), 'harloo', 'basic')
        }

        self.entity = PhysicsEntity(pos=(120, 30), name='side', action='idle')
        self.e_speed = 1.5
        self.timers = []

    def sub_update(self):

        self.timers = Timer.update_timers(self.timers)

        if self.handler.inputs['pressed'].get('mouse3'):
            self.timers.append(Timer(60))

        self.handler.canvas.fill((20, 20, 20))
        self.handler.canvas.blit(self.surf, self.handler.inputs['mouse pos'])

        # Update Buttons
        for key, btn in self.buttons.items():
            btn.update(self.handler.inputs)
            btn.render(self.handler.canvas)

        self.entity.vel = [0, 0]
        if self.handler.inputs['held'].get('a'):
            self.entity.vel[0] -= self.e_speed
            self.entity.animation.flip[0] = True
        elif self.handler.inputs['held'].get('d'):
            self.entity.vel[0] += self.e_speed
            self.entity.animation.flip[0] = False
        if self.handler.inputs['held'].get('w'):
            self.entity.vel[1] -= self.e_speed
        elif self.handler.inputs['held'].get('s'):
            self.entity.vel[1] += self.e_speed

        if any(self.entity.vel):
            self.entity.animation.set_action('run')
        else:
            self.entity.animation.set_action('idle')

        self.entity.update((self.buttons['hello'].rect, ))
        self.entity.render(self.handler.canvas)

        text = [f'{round(self.handler.clock.get_fps())} fps',
                f'{self.entity.vel}',
        str(list(self.timers))]
        self.handler.canvas.blit(FONTS['basic'].get_surf('\n'.join(text)), (0, 0))
