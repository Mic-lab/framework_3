# from .screen import screen
import pygame

def load_img(path, colorkey=(0, 0, 0)):
    img = pygame.image.load(path).convert()
    img.set_colorkey(colorkey)
    return img
    # return pygame.transform.scale_by(img, SCALE)

def read_file(path):
    with open(path) as f:
        content = f.read()
    return content
