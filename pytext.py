#!/usr/bin/env python

"""
Should only be tested on a RPi with raspbian on it.
"""

import pygame
import time
import textwrap
import random

def main():
  pygame.init()
  pygame.mouse.set_visible(False)
  resolution = [640, 480]
#  resolution = [1920, 1080]
  text = 'o    o---o-10------o-20------o-30------o-40------o-50------o-60------o-70---80-X'
  font = pygame.font.Font(fontpath, 14)
  size = font.size(text)
  rendera = font.render(text, 0, [0,255,0], [0,20,0])
  screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
  screen.fill([0,10,0])
  for i in range(1,26):
    print_rad(screen, i, text)

  distsleep(screen, 15)
  pygame.display.update()

def print_rad(screen, row, txt):
  fontpath = '/usr/share/fonts/truetype/freefont/FreeMono.ttf'
  font = pygame.font.Font(fontpath, 14)
  textp = ''
  for i in textwrap.wrap(txt, len(txt)/6):
    texty = textp + i
    textp = texty
    rendera = font.render(texty, 0, [0,255,0], [0,20,0])
    screen.blit(rendera, [0,1 + (row * 14)])
    rendera = font.render('o ' + str(row), 0, [187,187,0], [0,20,0])
    screen.blit(rendera, [0,1 + (row * 14)])
    pygame.display.update()
    if 1 == random.randint(1,28):
      distortion(screen)
    usleep(random.randint(1,20))

def distortion(screen):
  scroll=random.randint(5,20)
  if random.randint(0,1) == 0:
    xscroll=scroll
    yscroll=0
  else:
    xscroll=0
    yscroll=scroll
  screen.scroll(xscroll,yscroll)
  pygame.display.update()
  usleep(random.randint(20,50))
  screen.scroll(-xscroll,-yscroll)
  pygame.display.update()

def distsleep(screen,secs):
  timepassed=0
  while secs*1000 > timepassed:
    distortion(screen)
    waiting = random.randint(200,2020)
    usleep(waiting)
    timepassed += waiting
    print_rad(screen, 27, 'o    oxxxxxxxxx ' + str(timepassed) + ' --> ' + str(secs) + '000')

def usleep(ms):
  time.sleep(ms/1000.0)

if __name__ == '__main__': main()
