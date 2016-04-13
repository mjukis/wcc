#!/usr/bin/env python

"""
Should only be tested on a RPi with raspbian on it.
"""

import pygame
import time
import textwrap
import random
import sys
import os
import datetime
import MySQLdb
from vars import *

#global late
late = False

def main():
  global late
  pygame.init()
  pygame.mouse.set_visible(False)
  resolution = [640, 480]
  imgpath = './testcardt.jpg'
  fontpath = './AtariST8x16SystemFont.ttf'
  font = pygame.font.Font(fontpath, 18)
  screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
  screen.fill([0,20,0])

  inforad = " Opening Hours"
  inforad2 = "v2.1 "
  infolen = 53 - len(inforad) - len(inforad2)
  radpad = " " * infolen
  infoout = inforad + radpad + inforad2
  brad = footer
  blen = 53 - len(brad)
  bpad = " " * blen
  bout = bpad + brad
  print_rad(screen, 0, infoout,"TIT")
  print_rad(screen, 26, bout,"TIT")
#  print_rad(screen, 2, "This is testing")
#  print_rad(screen, 3, "This is bold testing","BOLD")
  arg = 24
  for argn in sys.argv:
      if argn.isdigit():
          arg = int(argn)

  nowwhen = datetime.datetime.fromtimestamp(time.time())
  global hm
  hm = int(nowwhen.strftime("%H%M"))
  if hm < 300:
    hm = hm + 2400
    arg = arg - 1

  hoursbyday(screen,datetime.date(2016,9,arg))
  distsleep(screen, dtime)
  img = pygame.image.load(imgpath)
  screen.blit(img,(0,0))
  pygame.display.flip()
  distsleep(screen, 1, False)
  pygame.display.update()

def print_rad(screen, row, txt, tag = False):
  fontpath = './AtariST8x16SystemFont.ttf'
  font = pygame.font.Font(fontpath, 18)
  textp = ''
  fg_base = [180,255,180]
  bg_base = [0,20,0]
  fg = fg_base
  bg = bg_base
  if tag == "TIT":
     font = pygame.font.Font(fontpath, 24)
     fg = bg_base
     bg = fg_base
  if tag == "INV":
     fg = bg_base
     bg = fg_base
  if tag == "BOLD":
     fg = [255,255,255]
     bg = bg_base
  for i in textwrap.wrap(txt, len(txt)/6):
    texty = textp + i
    textp = texty
    rendera = font.render(txt, 0, fg, bg)
    screen.blit(rendera, [0,1 + (row * 17)])
    pygame.display.update()
    if 1 == random.randint(1,28):
      distortion(screen)
    usleep(random.randint(1,20))

def distortion(screen):
#  scroll=random.randint(5,20)
  scroll=random.randint(1,3)
  if random.randint(0,1) == 0:
    xscroll=scroll
    yscroll=0
  else:
    xscroll=0
    yscroll=scroll
  for i in range(random.randint(1,20)):
     screen.scroll(xscroll,yscroll)
     pygame.display.update()
     usleep(random.randint(20,50))
     screen.scroll(-xscroll,-yscroll)
     pygame.display.update()

def distsleep(screen,msecs,counter=True):
  timepassed=0
  while msecs > timepassed:
    distortion(screen)
    waiting = random.randint(200,2020)
    usleep(waiting)
    timepassed += waiting
    if counter == True:
       print_rad(screen, 26, 'T' + str(timepassed) + ' --> ' + str(msecs),"TIT")

def usleep(ms):
  time.sleep(ms/1000.0)

#if __name__ == '__main__': main()

# WASTELAND EVENT SCHEDULER
# By Erik N8MJK

def schedule(screen,when,row):
    weekday = when.strftime("%a")
    daymon = when.strftime("%d%b")
    daytitle = " " + weekday.upper() + " " + daymon.upper() + "          LOCATION    STATUS"
    
    print_rad(screen,int(row),daytitle,"BOLD")

def hoursbyday(screen,when):
    global hm
    ri = 3
    schedule(screen,when,2)
    day = int(when.strftime("%d"))
    db = MySQLdb.connect("localhost","root","radiowave","wcc")
    cquery = "SELECT * FROM hours WHERE day = " + str(day) + " and close < " + str(hm) + " ORDER BY close"
    oquery = "SELECT * FROM hours WHERE day = " + str(day) + " and open <= " + str(hm) + " and close >= " + str(hm) + " ORDER BY close"
    nquery = "SELECT * FROM hours WHERE day = " + str(day) + " and open > " + str(hm) + " ORDER BY open"
    ccur = db.cursor()
    ocur = db.cursor()
    ncur = db.cursor()
    ccur.execute(cquery)
    ocur.execute(oquery)
    ncur.execute(nquery)
    crow = ccur.fetchone()
    orow = ocur.fetchone()
    nrow = ncur.fetchone()
#    db.close()
    prevtime = ""
    nowwhen = datetime.datetime.fromtimestamp(time.time())
    while crow is not None:
      place = crow[0]
      tquery = "SELECT * from hours WHERE day = " + str(day + 1) + " AND name = '" + place + "';"
      tcur = db.cursor()
      tcur.execute(tquery)
      trow = tcur.fetchone()
      if trow == None:
        tstr = "next year :("
      else:
        open = trow[2]
        if int(open) > 2359:
          openp = str(int(open) - 2400).zfill(4)
        else:
          openp = str(open).zfill(4)
        tstr = openp[:2] + ":" + openp[2:] + " tomorrow"
      pad = (28 - len(place)) * " "
      placestr = pad + place
      print_rad(screen, ri, placestr + " is CLOSED until " + tstr)
      ri = ri + 1
      crow = ccur.fetchone()
    db.close() 
    if ri != 3:
      ri = ri + 1
    while orow is not None:
      place = orow[0]
      close = orow[3]
      closetime = int(close) - int(hm)
      if closetime > 10:
        closep = str(close)
        if int(close) > 2359:
          closep = str(int(close) - 2400).zfill(4)
        if closetime > 99:
          closetime = int(round(closetime,-2)) / 100
          plural = "s"
          if closetime == 1:
            plural = ""
          closestr = str(closetime) + " more hour" + plural
        else:
          plural = "s"
          if closetime == 1:
            plural = ""
          closestr = str(closetime) + " more minute" + plural
        pad = (28 - len(place)) * " "
        placestr = pad + place
        print_rad(screen, ri, placestr + " is OPEN   until " + closep[:2] + ":" + closep[2:] + " (" + closestr + ")")
      else:  
        pad = (28 - len(place)) * " "
        placestr = pad + place
        print_rad(screen, ri, placestr + " is CLOSING NOW!")
      ri = ri + 1
      orow = ocur.fetchone()
    if ri != 3:
      ri = ri + 1
    while nrow is not None:
      place = nrow[0]
      open = nrow[2]
      opentime = int(close) - int(hm)
      if int(open) > 2359:
        openp = str(int(open) - 2400).zfill(4)
      else:
        openp = str(open)
      if opentime > 59:
        opentime = int(round(opentime,-2)) / 100
        plural = "s"
        if opentime == 1:
          plural = ""
        openstr = str(opentime) + " hour" + plural
      else:
        plural = "s"
        if opentime == 1:
          plural = ""
        openstr = str(opentime) + " minute" + plural
 
      pad = (28 - len(place)) * " "
      placestr = pad + place
      print_rad(screen, ri, placestr + " is CLOSED until " + openp[:2] + ":" + openp[2:] + " (in " + openstr + ")")
      ri = ri + 1
      nrow = ncur.fetchone()
    ri = ri + 1

if __name__ == '__main__': main()
