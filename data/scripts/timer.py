class Timer:

    def __init__(self, duration):
        self.frame = 0
        self.duration = duration
        self.done = False

    def update(self):
        self.frame += 1
        self.done = self.frame == self.duration

    @property
    def ratio(self):
        return self.frame / self.duration

    def __repr__(self):
        return f'<Timer({self.frame}/{self.duration})>'

    @staticmethod
    def update_timers(timers):
        new_timers = []
        for timer in timers:
            if not timer.done:
                new_timers.append(timer)
            timer.update()
        return new_timers
