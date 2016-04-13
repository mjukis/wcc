#!/usr/bin/python

import os
import time
import datetime

def top(iterations):
   i = 0
   while i < iterations: 
       x = os.system('top -b -d5|head -n 25')
       i = i + 1

def pic(pic,delay):
   string = "fbi -d /dev/fb0 -t " + str(delay) + " -noverbose -a -1 " + pic
   x = os.system(string)

def vid(vid):
   string = "omxplayer --no-osd -b " + vid
   stringdate = "omxplayer --no-osd -b WWDates.mp4"
   x = os.system(stringdate)
   x = os.system(string)

a = 0
while 1:
    day = time.strftime("%d")    
    if int(day) < 24:
        day = "25"
    if int(day) > 27:
        day = "27"
    x = os.system('clear')
    pic("testcard.jpg",5)
    x = os.system('clear')
    vid("WW2015Furious.mp4")
    x = os.system('clear')
    pic("testcard.jpg",5)
    x = os.system('clear')
    vid("Jugger.mp4")
    x = os.system('clear')
    pic("testcard.jpg",5)
    x = os.system('clear')
    vid("WW2015Teaser.mp4")
    x = os.system('clear')
    pic("testcard.jpg",5)
    x = os.system('clear')
    vid("WW2014Official.mp4")
    x = os.system('clear')
    pic("testcard.jpg",5)
    x = os.system('clear')
    vid("WW2013Official.mp4")
    x = os.system('clear')
    time.sleep(0.1)
    a = a + 1
    
