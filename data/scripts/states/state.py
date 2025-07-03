from abc import abstractmethod

class State:

    def __init__(self, game_handler):
        self.handler = game_handler

    @abstractmethod
    def update(self):
        pass
