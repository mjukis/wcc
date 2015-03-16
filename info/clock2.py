#!/usr/bin/python

import Image, ImageDraw, ImageFilter, ImageFont
import time
import math

imt = Image.open("clockface2.png")
im = imt.convert("RGB")
dr = ImageDraw.Draw(im)
font = ImageFont.truetype("hl45.ttf",35)

cx = int(im.size[0]) / 2
cy = int(im.size[1]) / 2
min = int(time.strftime("%M"))
hour = int(time.strftime("%I"))
mtime = time.strftime("%H%M")
mina = min * 6
houra = 0.5 * (60 * hour + min)

ntime = mtime[0] + " " + mtime[1] + " : " + mtime[2] + " " + mtime[3]

minx = cx + 140 * math.cos(math.radians(mina - 90))
miny = cy + 140 * math.sin(math.radians(mina - 90))
hourx = cx + 90 * math.cos(math.radians(houra - 90))
houry = cy + 90 * math.sin(math.radians(houra - 90))
color = "hsl(0,0%,100%)"
dr.line((cx,cy,hourx,houry),"black",width=5)
dr.line((cx,cy,minx,miny),"black",width=3)
for a in range (1,13):
   thisa = a * 30
   thisix = cx + 100 * math.cos(math.radians(thisa))
   thisiy = cy + 100 * math.sin(math.radians(thisa))
   thisox = cx + 130 * math.cos(math.radians(thisa))
   thisoy = cy + 130 * math.sin(math.radians(thisa))
   dr.line((thisox,thisoy,thisix,thisiy),"black")

dr.ellipse(((cx-8,cy-8),(cx+8,cy+8)),fill="black")
dr.ellipse(((hourx-5,houry-5),(hourx+5,houry+5)),fill="black")
dr.ellipse(((minx-3,miny-3),(minx+3,miny+3)),fill="black")

w,h=dr.textsize(ntime,font=font)

dr.text((cx-w/2,48),ntime,"black",font)

#dr.line((0,0,100,100),"yellow")

#im1 = im.filter(ImageFilter.BLUR)
im.save("clock2.png")
