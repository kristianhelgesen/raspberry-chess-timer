

import urllib
import httplib2
import sys
import os
import Image
import xml.etree.ElementTree as ET
import ImageDraw
import Image
#import ImageFont

import time
import threading
from datetime import datetime
from datetime import timedelta


from EPD import EPD
from timerthread import TimerThread


COLW = 64
WHITE = 1
BLACK = 0

# fonts are in different places on Raspbian/Angstrom so search
possible_fonts = [
                  '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSansMono-Bold.ttf',   # R.Pi
                  '/usr/share/fonts/truetype/freefont/FreeMono.ttf',                # R.Pi
                  ]

FONT_FILE = ''
for f in possible_fonts:
    if os.path.exists(f):
        FONT_FILE = f
        break

#if '' == FONT_FILE:
#    raise 'no font file found'

CLOCK_FONT_SIZE = 40
DATE_FONT_SIZE  = 30
MAX_START = 0xffff


class ChessTimer:
    def __init__(self):
        self.isPlaying = True
        self.isInitialized = False
        self.gameduration = timedelta(seconds=14)
        self.incrementFunction = self.incrementFunctionNone


    def tickCallbackWhite(self,remaining):
        print 'white '+remaining


    def tickCallbackBlack(self,remaining):
        print 'black '+remaining


    def gameOverWhite(self):
        print 'black wins!'
        self.isPlaying = False


    def gameOverBlack(self):
        print 'white wins!'
        self.isPlaying = False


    def incrementFunctionNone(self):
        return

    def newWhiteTimer(self):
        return TimerThread(self.gameduration, self.incrementFunction, self.tickCallbackWhite, self.gameOverWhite)

    def newBlackTimer(self):
        return TimerThread(self.gameduration, self.incrementFunction, self.tickCallbackBlack, self.gameOverBlack)

    def onButton1(self):
        if self.isPlaying:
            if not self.isInitialized:
                self.player1Timer = self.newWhiteTimer()
                self.player2Timer = self.newBlackTimer()
                self.player1Timer.start()
                self.player2Timer.start()
                self.isInitialized = True
            self.player1Timer.resume()


    def offButton1(self):
        if self.isPlaying:
            self.player1Timer.pause()


    def onButton2(self):
        if self.isPlaying:
            if not self.isInitialized:
                self.player1Timer = self.newBlackTimer()
                self.player2Timer = self.newWhiteTimer()
                self.player1Timer.start()
                self.player2Timer.start()
                self.isInitialized = True
            self.player2Timer.resume()


    def offButton2(self):
        if self.isPlaying:
            self.player2Timer.pause()




def main():

    chessTimer = ChessTimer()
    chessTimer.onButton1()
    time.sleep(3)
    chessTimer.offButton1()

    chessTimer.onButton2()
    time.sleep(4)
    chessTimer.offButton2()

    chessTimer.onButton1()
    time.sleep(3)
    chessTimer.offButton1()

    chessTimer.onButton2()
    time.sleep(4)
    chessTimer.offButton2()

    exit()





def timertest():
    gameduration = timedelta(seconds=14)

    whiteTimer = TimerThread(gameduration, incrementFunction, tickCallbackWhite, gameOverWhite)
    whiteTimer.start()

    time.sleep(3.1)
    whiteTimer.resume()
    print('2')
    time.sleep(5.2)

    whiteTimer.pause()
    print('3')
    time.sleep(3.3)

    whiteTimer.resume()
    print('4')
    time.sleep(5.4)

    print('exiting')

    exit()

#    t = threading.Thread(target=timer_worker,kwargs= {'a':100,'b':'b'})
#    t.start()


#    epd = EPD()
    
#   image = Image.new('1', epd.size, WHITE)
#   draw = ImageDraw.Draw(image)
#   width, height = image.size 
#   draw.rectangle((0, 0, width, height), fill=WHITE, outline=WHITE)
    
#   font = ImageFont.truetype('fonts/LiberationSans-Regular.ttf', 12)
    


#   epd.clear()
#   epd.display(image)
#   epd.update()
    








if __name__ == '__main__':
    main()







