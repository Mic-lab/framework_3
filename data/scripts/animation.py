import pygame
import os
from . import utils
from pprint import pprint

class Animation:

    ANIMATIONS_DIR = 'data/imgs/animations'

    @staticmethod
    def load_spritesheet(config, spritesheet: pygame.Surface):
        spritesheet_data = {}

        for frame in config['frames']:

            # filename is action

            if not frame['filename']:  # Untagged
                continue

            if frame['filename'] not in spritesheet_data:
                spritesheet_data[frame['filename']] = []
                                                      
            frame_rect = pygame.Rect(
                frame['frame']['x'],
                frame['frame']['y'],
                frame['frame']['w'],
                frame['frame']['h'],
            )

            frame_img = spritesheet.subsurface(frame_rect)
            spritesheet_data[frame['filename']].append(
                {'img': frame_img,
                 'duration': frame['duration'] // (100/6)}  # convert ms to frames at 60 FPS
            )

        return spritesheet_data

    @classmethod
    def load_db(cls):
        cls.animation_db = {}
        cls.img_db = {}

        directory = cls.ANIMATIONS_DIR
            
        for file in os.listdir(directory):
            file_name = os.fsdecode(file)
            if file_name.endswith('.png'): 
                animation_name = file_name.split('.')[0]
                config_location = os.path.join(directory, animation_name + '.json')
                try:
                    animation_config = utils.read_json(config_location)
                except FileNotFoundError:
                    # No json file means it's a static image
                    img = utils.load_img(os.path.join(directory, file_name))
                    cls.animation_db[animation_name] = {None: img}  # So that Animation can find it easily
                    cls.img_db[animation_name] = img                # For ease of access outside of the class
                else:
                    spritesheet = utils.load_img(os.path.join(directory, file_name))
                    spritesheet_data = cls.load_spritesheet(animation_config, spritesheet)
                    cls.animation_db[animation_name] = spritesheet_data
            else:
                continue

    def __init__(self, name, action, flip=[False, False]):
        self.name = name
        self.action = None
        self.set_action(action, reset=True)
        self.flip = flip

    @property
    def img(self):
        base_img = self.frame['img']
        if any(self.flip):
            base_img = pygame.transform.flip(base_img, *self.flip)
        return base_img

    @property
    def frames(self):
        return Animation.animation_db[self.name][self.action]

    @property
    def frame(self):
        return self.frames[self.animation_frame]

    def update(self):
        if self.action is None:
            return

        self.game_frame += 1
        if self.game_frame > self.frame['duration']:
            self.game_frame = 0
            self.animation_frame += 1
            if self.animation_frame >= len(self.frames):
                self.animation_frame = 0
                return True

    def set_action(self, new_action, reset=False):
        if self.action and new_action == self.action and not reset:
            return

        self.action = new_action
        self.animation_frame = 0
        self.game_frame = 0

Animation.load_db()

pprint(Animation.animation_db)
