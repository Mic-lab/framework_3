class Timer:

    def __init__(self, duration):
        self.frame = 0
        self.duration = duration
        self.done = False

    def update(self):
        self.frame += 1
        self.done = self.frame == self.duration

    def __repr__(self):
        return f'<Timer({self.frame})>'
