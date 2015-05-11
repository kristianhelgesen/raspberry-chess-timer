import time
import threading
from datetime import datetime
from datetime import timedelta


class TimerThread(threading.Thread):
    def __init__(self, duration, tickCallback, gameOverCallback):
        threading.Thread.__init__(self)
        self.remaining = duration

        self.tickCallback = tickCallback
        self.gameOverCallback = gameOverCallback

        self.daemon = True
        self.paused = True
        self.state = threading.Condition()

    def run(self):
        remainingStr = ''
        while True:
            with self.state:
                if self.paused:
                    self.state.wait() # block until notified


            # sleeping and recording lenght of pause. (this can be interrupted)
            before = datetime.now()
            with self.state:
                self.state.wait(0.05)
            slept = datetime.now() - before
            self.remaining -= slept


            hours, remainder = divmod(self.remaining.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
#            remainingStr1 = '%d:%2d:%2d' % (hours, minutes, seconds)
            if hours > 0:
                remainingStr1 = "{:.0f}:{:0>2d}:{:0>2d}".format(hours, minutes, seconds)
            else:
                remainingStr1 = "{:0>2d}:{:0>2d}".format(minutes, seconds)


            if remainingStr!=remainingStr1:
                # update screen
                remainingStr = remainingStr1
                self.tickCallback(remainingStr)


            if self.remaining < timedelta(seconds=0):
                self.gameOverCallback()
                break

            # if pause is called when sleeping
            with self.state:
                if self.paused:
                    continue




    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()  # unblock self if waiting

    def pause(self):
        with self.state:
            self.paused = True  # make self block and wait
            self.state.notify()  # unblock self if waiting

