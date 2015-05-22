

import urllib
import httplib2
import sys
import os
import Image
import xml.etree.ElementTree as ET
import ImageDraw
import Image
import ImageFont

import time
import threading
from datetime import datetime
from datetime import timedelta


from EPD import EPD
from timerthread import TimerThread

import RPi.GPIO as GPIO


COLW = 64
WHITE = 1
BLACK = 0

textfont = ImageFont.truetype('fonts/LiberationSans-Regular.ttf', 60)
chessfont = ImageFont.truetype('fonts/CASEFONT.TTF', 45)


CLOCK_FONT_SIZE = 40
DATE_FONT_SIZE  = 30
MAX_START = 0xffff

epd = EPD()
image = Image.new('1', epd.size, WHITE)
draw = ImageDraw.Draw(image)
width, height = image.size 


games = [
    {
        'name':'Fischer',
        'duration':timedelta(seconds=600),
    },
    {
        'name':'Bronstein',
        'duration':timedelta(seconds=600),
    },
    {
        'name':'Simple delay',
        'duration':timedelta(seconds=600),
    },
]

# games[0]['name']






class ChessTimer:
    def __init__(self):

        self.isPlaying = True
        self.isInitialized = False
        self.gameduration = timedelta(seconds=5600)
        self.incrementFunction = self.incrementFunctionNone



    def tickCallbackWhite(self,remaining):
        if remaining['seconds']%5==0 or 'forceUpdate' in remaining:
            remainingStr = self.formatTime(remaining)
            print 'white '+remainingStr
            threading.Thread(target=self.writeRemainigWhite,args=(remainingStr,'')).start()


    def writeRemainigWhite(self,remainingStr,test):
        draw.rectangle((0,0, width - 5, height/2), fill=WHITE, outline=WHITE)
        draw.rectangle((0,height/2, 60, height), fill=BLACK, outline=BLACK)
        draw.text((5,25), "q", font=chessfont)
        draw.text((90-5*len(remainingStr),10), remainingStr, font=textfont)
        epd.display(image)
        epd.partial_update()


    def tickCallbackBlack(self,remaining):
        if remaining['seconds']%5==0 or 'forceUpdate' in remaining:
            remainingStr = self.formatTime(remaining)
            print 'black '+remainingStr
            threading.Thread(target=self.writeRemainigBlack,args=(remainingStr,'')).start()


    def writeRemainigBlack(self,remainingStr,test):
        draw.rectangle((0,height/2, width, height), fill=BLACK, outline=BLACK)
        draw.rectangle((0,0, 60, height/2), fill=WHITE, outline=WHITE)
        draw.text((5,105), "q", font=chessfont, fill=WHITE)
        draw.text((90-5*len(remainingStr),95), remainingStr, font=textfont,fill=WHITE)
        epd.display(image)
        epd.partial_update()


    def formatTime(self,remaining):
        hours = remaining['hours']
        minutes = remaining['minutes']
        seconds = remaining['seconds']

        if hours > 0:
            remainingStr = "{:.0f}:{:0>2d}:{:0>2d}".format(hours, minutes, seconds)
        else:
            remainingStr = "{:0>2d}:{:0>2d}".format(minutes, seconds)
        return remainingStr


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

    
    def button1Event(self, channel):
        if GPIO.input(3):
            self.offButton1()
        else:             
            self.onButton1()

    def onButton1(self):
        if self.isPlaying:
            if not self.isInitialized:
                self.player1Timer = self.newWhiteTimer()
                self.player2Timer = self.newBlackTimer()
                self.player2Timer.start()
                self.player1Timer.start()
                self.isInitialized = True
            self.player1Timer.resume()

    def offButton1(self):
        if self.isPlaying:
            self.player1Timer.pause()
            remaining = self.player1Timer.remainingTime()
            remaining['forceUpdate'] = True
            self.player1Timer.tickCallback(remaining)


    def button2Event(self, channel):
        if GPIO.input(3):
            self.offButton2()
        else:             
            self.onButton2()

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
            remaining = self.player2Timer.remainingTime()
            remaining['forceUpdate'] = True
            self.player2Timer.tickCallback(remaining)





class Display:

    def __init__(self):
        self.textfont = ImageFont.truetype('fonts/LiberationSans-Regular.ttf', 60)
        self.chessfont = ImageFont.truetype('fonts/CASEFONT.TTF', 45)




def main():

    draw.rectangle((0, 0, width, height), fill=WHITE, outline=WHITE)
    
    chessfont = ImageFont.truetype('fonts/CASEFONT.TTF', 100)
    
    draw.text((5,5), "q", font=chessfont)

    epd.clear()
    epd.display(image)
    epd.update()

#    try:  
    print "starting chess timer"
    chessTimer = ChessTimer()

    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(3, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(5, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(3, GPIO.BOTH, callback=chessTimer.button1Event, bouncetime=300)
    GPIO.add_event_detect(5, GPIO.BOTH, callback=chessTimer.button2Event, bouncetime=300)



    while True:
        print "waiting"
        time.sleep(10)
  
#    except KeyboardInterrupt:  
        # here you put any code you want to run before the program   
        # exits when you press CTRL+C  
#       print "Chess timer done\n",  # print value of counter  
      
#    except:  
        # this catches ALL other exceptions including errors.  
        # You won't get any error messages for debugging  
        # so only use it once your code is working  
 #       print "Other error or exception occurred!"  
      
 #   finally:  
#        GPIO.cleanup() # this ensures a clean exit  
#        time.sleep(1)
#        exit()




#    chessTimer.onButton1()
#    time.sleep(6)
#    chessTimer.offButton1()

#    chessTimer.onButton2()
#    time.sleep(31)
#    chessTimer.offButton2()

#   chessTimer.onButton1()
#    time.sleep(3)
#    chessTimer.offButton1()

#    chessTimer.onButton2()
#    time.sleep(4)
#    chessTimer.offButton2()



    








if __name__ == '__main__':
    main()







