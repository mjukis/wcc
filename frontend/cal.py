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

global late
late = False

def main():
  pygame.init()
  pygame.mouse.set_visible(False)
  resolution = [640, 480]
  imgpath = './testcardt.jpg'
  fontpath = './AtariST8x16SystemFont.ttf'
  font = pygame.font.Font(fontpath, 18)
  screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
  screen.fill([0,0,0])

  inforad = " Schedule of Events"
  radpad = " " * (53 - len(inforad))
  infoout = inforad + radpad
  print_rad(screen, 0, infoout,"TIT")
#  print_rad(screen, 2, "This is testing")
#  print_rad(screen, 3, "This is bold testing","BOLD")
  arg = 24
  for argn in sys.argv:
      if argn.isdigit():
          arg = int(argn)

  nowwhen = datetime.datetime.fromtimestamp(time.time())
  thishour = int(nowwhen.strftime("%H"))
  if thishour < 5:
      late = True
      arg = arg - 1

  eventsbyday(screen,datetime.date(2016,9,arg))
  distsleep(screen, 5)
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

def distsleep(screen,secs,counter=True):
  timepassed=0
  while secs*1000 > timepassed:
    distortion(screen)
    waiting = random.randint(200,2020)
    usleep(waiting)
    timepassed += waiting
    if counter == True:
       print_rad(screen, 27, 'o    oxxxxxxxxx ' + str(timepassed) + ' --> ' + str(secs) + '000')

def usleep(ms):
  time.sleep(ms/1000.0)

#if __name__ == '__main__': main()

# WASTELAND EVENT SCHEDULER
# By Erik N8MJK

def schedule(screen,when,row):
    weekday = when.strftime("%a")
    daymon = when.strftime("%d%b")
    daytitle = " " + weekday.upper() + "    " + daymon.upper() + "    EVENT"
    print_rad(screen,int(row),daytitle,"BOLD")

def eventsbyday(screen,when):
    global late
    ri = 3
    schedule(screen,when,2)
    day = int(when.strftime("%d"))
    lowlimit = day * 100000000 + 7000000;
    highlimit = (day + 1) * 100000000 + 3010000;
    db = MySQLdb.connect("localhost","root","radiowave","wcc")
    query = "SELECT * FROM eventlist WHERE id > " + str(lowlimit) + " and id < " + str(highlimit) + " ORDER BY id"
    cur = db.cursor()
    cur.execute(query)
    row = cur.fetchone()
    db.close()
    timebar = False
    prevtime = ""
    while row is not None:
        nowwhen = datetime.datetime.fromtimestamp(time.time())
        nowtime = nowwhen.strftime("%H%M")

#        time.sleep(0.1)
        eventdate = row[0][:2]
        eventcat = row[0][6]
        if int(eventdate) != int(day):
            if late == False and timebar == False:
                timebar = True
                print_rad(screen,ri,"-" + nowtime + "-----------------------------------------------------------------")
                ri = ri + 1        
            when2 = datetime.date(2016,9,int(eventdate))
            ri = ri + 1
            schedule(screen,when2,ri)
            ri = ri + 1
            day = eventdate
            if late == True:
                late = False
            
        eventtime = row[0][2:6]
        eventwhen = datetime.datetime(2016,9,int(eventdate),int(eventtime[:2]),int(eventtime[2:4]))
        nowwhen = datetime.datetime.fromtimestamp(time.time())
        nowtime = nowwhen.strftime("%H%M")
        eventustime = eventwhen.strftime("%I:%M%p")
        if eventustime[0] == "0":
            prettyustime = " " + eventustime.lstrip("0")
        else:
            prettyustime = eventustime
        eventtext = row[1]
        if eventcat == "0":
            eventtext = ""
        if eventcat == "5":
            eventtext = "LIVE! " + eventtext + " @ Main Stage"
        if int(nowtime) < int(eventtime) and timebar == False:
            if late == False:
                timebar = True
                print_rad(screen, ri, "-" + nowtime + "-----------------------------------------------------------------")
                ri = ri + 1        
        if str(eventtime) == prevtime:
            print_rad(screen, ri, "                 " + eventtext)
            ri = ri + 1        
        else:
            print_rad(screen,ri," " + str(eventtime) + " " + prettyustime + "    " + eventtext)
            ri = ri + 1        
        prevtime = str(eventtime)
        row = cur.fetchone()
    if timebar == False and prevtime != "":
        print_rad(screen,ri,"-" + nowtime + "-----------------------------------------------------------------")
        ri = ri + 1

if __name__ == '__main__': main()
