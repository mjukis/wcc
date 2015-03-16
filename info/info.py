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
   string = "fbi -d /dev/fb0 -t " + str(delay) + " -noverbose -a -1 /home/pi/myrepos/wcc/info/" + pic
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
    x = os.system('/home/pi/myrepos/wcc/info/cal.py ' + day)
    time.sleep(15)
    x = os.system('/home/pi/myrepos/wcc/info/hours.py ' + day)
    time.sleep(15)
    x = os.system('clear')
    x = os.system('/home/pi/myrepos/wcc/info/clock2.py')
    pic("clock2.png",15)
    x = os.system('clear')
    x = os.system('/home/pi/myrepos/wcc/info/rad.py ' + day)
    time.sleep(15)
    x = os.system('clear')
    time.sleep(0.1)
    a = a + 1
    
