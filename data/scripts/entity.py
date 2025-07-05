import pygame
from pygame import Vector2
from .animation import Animation

class Entity:
    
    def __init__(self, pos, name, action=None):
        self.pos = Vector2(pos)
        self.name = name
        self.animation = Animation(name, action)
        self.flip = [False, False]

    @property
    def rect(self) -> pygame.Rect:
        return self.animation.rect

    @property
    def img(self) -> pygame.Surface:
        return self.animation.img

    def update(self):
        self.animation.update()

    def render(self, surf):
        rect = pygame.Rect(self.rect.x+self.pos[0], self.rect.y+self.pos[1], *self.rect.size)
        pygame.draw.rect(surf, (150, 150, 200), rect)
        surf.blit(self.img, self.pos)

class PhysicsEntity(Entity):

    def __init__(self, vel=(0, 0), acceleration=(0, 0), max_vel=(9999, 9999), *args, **kwargs):
        self.__vel = Vector2(vel)
        self.acceleration = Vector2(acceleration)
        self.max_vel = Vector2(max_vel)
        super().__init__(*args, **kwargs)

    @property
    def vel(self):
        return self.__vel

    @vel.setter
    def vel(self, new_vel):
        self.last_vel = new_vel.copy()
        self.__vel = Vector2(new_vel)

    def update(self):
        super().update()

        self.pos += self.vel
        self.vel += self.acceleration
        if abs(self.vel.x) > self.max_vel.x: self.max_vel.x = self.max_vel.x / abs(self.max_vel).x * self.max_vel.x
        if abs(self.vel.y) > self.max_vel.y: self.max_vel.y = self.max_vel.y / abs(self.max_vel).y * self.max_vel.x
