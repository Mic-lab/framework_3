import pygame
from math import atan, pi
from pygame import Vector2
from .animation import Animation
    
class Entity:
    def __init__(self, pos, name, action=None):
        self._real_pos = Vector2(pos)
        self.name = name
        self.animation = Animation(name, action)
        self.flip = [False, False]

    @property
    def pos(self):
        return Vector2(int(self._real_pos[0]), int(self._real_pos[1]))

    def change_pos(self, change_vec):
        # Did not want to use a setter method because it wouldn't be
        # called if you only touch one axis (like pos.x += x)
        
        # self._real_pos = self.pos + change_vec 
        if change_vec.x:
            self._real_pos.x = self.pos.x + change_vec.x
        if change_vec.y:
            self._real_pos.y = self.pos.y + change_vec.y

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(*(self.animation.rect.topleft + self.pos), *self.animation.rect.size)

    @property
    def img(self) -> pygame.Surface:
        return self.animation.img

    def update(self):
        return self.animation.update()

    def render(self, surf):
        # pygame.draw.rect(surf, (255, 0, 0), self.rect)
        surf.blit(self.img, self.pos)

    def __repr__(self):
        return f'<{self.name}>'

class PhysicsEntity(Entity):

    def __init__(self, vel=(0, 0), acceleration=(0, 0), max_vel=(9999, 9999), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vel = Vector2(vel)
        self.acceleration = Vector2(acceleration)
        self.max_vel = Vector2(max_vel)
        self.collision_directions = {'up': False,
                                     'right': False,
                                     'down': False,
                                     'left': False}

    @property
    def angle(self):
        angle = self.vel.angle_to(Vector2(1, 0))
        return angle

    def update(self, rects=None):
        output = super().update()

        self.move(rects)
        self.vel += self.acceleration
        if abs(self.vel.x) > self.max_vel.x: self.max_vel.x = self.max_vel.x / abs(self.max_vel).x * self.max_vel.x
        if abs(self.vel.y) > self.max_vel.y: self.max_vel.y = self.max_vel.y / abs(self.max_vel).y * self.max_vel.x

        return output

    def move(self, rects):
        if not rects:
            self._real_pos += self.vel
            return

        self.collision_directions = {'up': False,
                                     'right': False,
                                     'down': False,
                                     'left': False}

        for axis in range(2):
            self.resolve_collisions(axis, rects)

    def resolve_collisions(self, axis, rects):
        self._real_pos[axis] += self.vel[axis]
        direction = None
        for rect in rects:
            if self.rect.colliderect(rect):
                if axis == 0:
                    if self.vel[0] > 0:
                        delta = self.rect.right - rect.left
                        direction = 'right'
                    elif self.vel[0] < 0:
                        delta = self.rect.left - rect.right
                        direction = 'left'
                    else:
                        delta = 0
                        print(f'[WARNING] {self} Didn\'t resolve collision last frame or rect changed sizes ({axis=})')
                elif axis == 1:
                    if self.vel[1] < 0:
                        delta = self.rect.top - rect.bottom
                        direction = 'top'
                    elif self.vel[1] > 0:
                        delta = self.rect.bottom - rect.top
                        direction = 'bottom'
                    else:
                        delta = 0
                        print(f'[WARNING] {self} Didn\'t resolve collision last frame or rect changed sizes ({axis=})')

                v = Vector2(0, 0)
                v[axis] = delta
                self.change_pos(-v)
                if direction: self.collision_directions[direction] = True
                return


