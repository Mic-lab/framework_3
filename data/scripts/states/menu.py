from .. import utils
from ..button import Button
from ..font import FONTS
from .. import animation
from ..entity import Entity, PhysicsEntity
from ..timer import Timer
from ..particle import Particle, ParticleGenerator
from .state import State
import pprint
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
        self.particle_gens = [ParticleGenerator.from_template((100, 200), 'angle test')]

    def sub_update(self):

        self.timers = Timer.update_timers(self.timers)

        if self.handler.inputs['pressed'].get('mouse3'):
            self.timers.append(Timer(60))

        self.handler.canvas.fill((20, 20, 20))

        if self.handler.inputs['pressed'].get('mouse1'):
            self.particle_gens.append(ParticleGenerator.from_template(self.handler.inputs['mouse pos'], 'smoke'))

        self.particle_gens = ParticleGenerator.update_generators(self.particle_gens)
        for particle_gen in self.particle_gens:
            particle_gen.render(self.handler.canvas)

        self.handler.canvas.set_at(self.handler.inputs['mouse pos'], (255, 0, 0))

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
                f'{self.entity.vel}']
        self.handler.canvas.blit(FONTS['basic'].get_surf('\n'.join(text)), (0, 0))
