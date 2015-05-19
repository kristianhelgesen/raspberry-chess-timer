import math
import time
import threading
from datetime import datetime
from datetime import timedelta


class TimerThread(threading.Thread):
    def __init__(self, duration, incrementFunction, tickCallback, gameOverCallback):
        threading.Thread.__init__(self)
        self.remaining = duration

        self.incrementFunction = incrementFunction
        self.tickCallback = tickCallback
        self.gameOverCallback = gameOverCallback


        self.daemon = True
        self.paused = True
        self.running = True
        self.state = threading.Condition()

        self.lastSec = 0
        self.tick()


    def run(self):
        while self.running:
            with self.state:
                if self.paused:
                    self.state.wait() # block until notified

            # sleeping and recording lenght of pause. (this can be interrupted)
            before = datetime.now()
            with self.state:
                self.state.wait(0.05)
            slept = datetime.now() - before
            self.remaining -= slept

            self.tick()

            if self.remaining < timedelta(seconds=0):
                self.gameOverCallback()
                break


    def tick(self):
        rem = self.remainingTime()
        hours, remainder = divmod(self.remaining.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        sec = int(math.floor(seconds))

        if self.lastSec != rem['seconds']:
            self.lastSec = rem['seconds']
            self.tickCallback(rem)


    def remainingTime(self):
        hours, remainder = divmod(self.remaining.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        sec = int(math.floor(seconds))

        return {
                'hours' : hours,
                'minutes' : minutes,
                'seconds' : sec
                }


    def resume(self):
        with self.state:
            self.incrementFunction();
            self.paused = False
            self.state.notify()  # unblock self if waiting

    def pause(self):
        with self.state:
            self.paused = True  # make self block and wait
            self.state.notify()  # unblock self if waiting

    def stop(self):
        self.running = False
        self.paused = False
        with self.state:
            self.state.notify()  # unblock self if waiting

