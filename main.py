import sys
import pygame
from data.scripts import config
from data.scripts import utils
from data.scripts.screen import screen
from data.scripts import mgl
from moderngl import TRIANGLE_STRIP
from data.scripts.states.menu import Menu

class GameHandler:

    def __init__(self):
        self.canvas = pygame.Surface(config.CANVAS_SIZE)
        self.clock = pygame.time.Clock()
        self.inputs = {'pressed': {}, 'released': {}, 'held': {}}

        self.set_state(Menu)

    def set_state(self, state):
        self.state = state(self)

    def handle_input(self):
        for key in self.inputs['pressed']:
            self.inputs['pressed'][key] = self.inputs['released'][key] = False

        mx, my = pygame.mouse.get_pos()
        self.inputs['mouse pos'] = (mx // config.SCALE, my // config.SCALE)
        self.inputs['unscaled mouse pos'] = mx, my

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.inputs['pressed'][f'mouse{event.button}'] = True
                self.inputs['held'][f'mouse{event.button}'] = True

            if event.type == pygame.MOUSEBUTTONUP:
                self.inputs['released'][f'mouse{event.button}'] = True
                self.inputs['held'][f'mouse{event.button}'] = False

            if event.type == pygame.KEYDOWN:
                key_name = pygame.key.name(event.key)
                self.inputs['pressed'][key_name] = True
                self.inputs['held'][key_name] = True

            if event.type == pygame.KEYUP:
                key_name = pygame.key.name(event.key)
                self.inputs['released'][key_name] = True
                self.inputs['held'][key_name] = False


    def run(self):
        self.running = True

        while self.running:
            self.handle_input()

            self.state.update()

            mgl.transfer_shader_surfs(
                {'canvasTex': self.canvas}
            )

            mgl.render_object.render(mode=TRIANGLE_STRIP)
            pygame.display.flip()
            mgl.release_textures()

            self.clock.tick(config.fps)

        pygame.quit()
        sys.exit()

GameHandler().run()
