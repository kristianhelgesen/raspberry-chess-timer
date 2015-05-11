

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
DATEFORMAT = "%Y-%m-%dT%H:%M:%S"



def timer_worker(a, b):
    remaining = a

    print('timer worker')
    print(a)


def tickCallback(remaining):
    print remaining

def gameOverWhite():
    print 'gameover for white'


def main():
    print('1')

    whiteTimer = TimerThread(timedelta(seconds=4), tickCallback, gameOverWhite)
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







