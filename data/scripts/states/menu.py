from .. import utils
from .state import State

class Menu(State):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.surf = utils.load_img('D:/image.png')

    def update(self):
        self.handler.canvas.fill((50, 0, 50))
        self.handler.canvas.blit(self.surf, self.handler.inputs['mouse pos'])
