import random
from .timer import Timer
from .entity import PhysicsEntity
from copy import deepcopy
from functools import lru_cache
import pygame
from pygame import Vector2

class Particle(PhysicsEntity):

    ANGLE_ROUNDING = 30
    cache = {}

    def __init__(self, pos=(0, 0), angled=False, *args, **kwargs):
        name = 'particles'
        super().__init__(pos=pos, name=name, *args, **kwargs)
        self.angled = angled
        self.alive = True

    @property
    def cache_key(self):
        if self.angled:
            return (self.animation.action, self.rounded_angle)

    @property
    def rounded_angle(self):
        return round(self.angle / Particle.ANGLE_ROUNDING) * Particle.ANGLE_ROUNDING

    @property
    def img(self):
        base_img = super().img
        if self.cache_key:
            if self.cache_key not in Particle.cache:
                Particle.cache[self.cache_key] = pygame.transform.rotate(base_img, self.rounded_angle)
            return Particle.cache[self.cache_key]

        return base_img

    def update(self, *args, **kwargs):
        self.alive = not super().update(*args, **kwargs)

    def copy(self):
        return deepcopy(self)

class ParticleGenerator:

    TEMPLATES = {
        'smoke': {
            'base_particle': Particle(action='basic', vel=(0, 0)),
            'vel_randomness': 0.5,
            'rate': 10
        },
        'angle test': {
            'base_particle': Particle(action='arrow', vel=(0, -2), acceleration=(0, 0.05), angled=True),
            'vel_randomness': 1,
            'rate': 5,
            'inverse_rate': True,
            'duration': None,
        }
    }

    @classmethod
    def from_template(cls, pos, template_key, **overwrites):
        config = ParticleGenerator.TEMPLATES[template_key]
        config = config | overwrites  # https://stackoverflow.com/questions/38987/how-do-i-merge-two-dictionaries-in-a-single-expression-in-python
        return cls(pos=pos, **config)

    def __init__(self, base_particle: Particle, pos, vel_randomness=1, duration=1, rate=1, inverse_rate=False):
        self.base_particle = base_particle
        self.pos = pos
        self.vel_randomness = vel_randomness
        self.duration = duration
        self.rate = rate
        self.inverse_rate = inverse_rate
        self.particles = []
        self.timer = Timer(duration)
        self.done = False

    def generate_particle(self):
        particle = self.base_particle.copy()
        particle._real_pos = self.pos - 0.5 * Vector2(particle.animation.size)
        vel_offset = random.uniform(0, self.vel_randomness) * Vector2(1, 0)
        vel_offset = vel_offset.rotate(random.uniform(0, 360))
        particle.vel += vel_offset
        return particle

    def update(self):
        if not self.timer.done:
            if not self.inverse_rate:
                for _ in range(self.rate):
                    self.particles.append(self.generate_particle())
            else:
                if self.timer.frame % self.rate == 0:
                    self.particles.append(self.generate_particle())

        new_particles = []
        for particle in self.particles:
            particle.update()
            if particle.alive:
                new_particles.append(particle)
        self.particles = new_particles

        self.done = self.timer.done and not self.particles
        if self.done:
            return True
        if not self.timer.done: self.timer.update()

    def render(self, surf):
        for particle in self.particles:
            particle.render(surf)

    @staticmethod
    def update_generators(generators):
        new_generators = []
        for generator in generators:
            if not generator.done:
                new_generators.append(generator)
            generator.update()
        return new_generators
