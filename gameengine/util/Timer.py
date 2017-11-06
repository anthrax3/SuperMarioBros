import time

timers = []

class Timer:
    def __init__(self, interval: int, callback, args=(), startNow=False, cycles=-1):
        self.interval = interval
        self.callback = callback
        self.args = args
        self.startNow = startNow
        self.maxCycles = cycles

        self.cycles = 0
        self.paused = False

    def getMillis(self):
        return int(time.time() * 1000)

    def tick(self):
        if self.startNow and self.cycles == 0:
            self.execute()

        elif self.getMillis() - self.previous >= self.interval:
            if not self.paused:
                self.execute()

            self.reset()
        return self

    def execute(self):
        self.callback(*self.args)
        self.cycles += 1

        if self.cycles == self.maxCycles:
            self.stop()

    def start(self):
        self.resume()
        if self not in timers:
            timers.append(self)
            self.reset()
        return self

    def stop(self):
        if self in timers:
            timers.remove(self)

    def reset(self):
        self.previous = self.getMillis()

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False


def updateTimers():
    for timer in timers:
        timer.tick()