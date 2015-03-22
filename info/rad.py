#!/usr/bin/python

# RADIO PROGRAM SCHEDULER
# By Erik N8MJK

import sys
import os
import time
import datetime
import MySQLdb

class color:
    BOLD = '\033[1m'
    END = '\033[0m'

global late
late = False

global track
trackt = "Nothing Playing?"
ntrackt = "Nothing Playing?"
db = MySQLdb.connect("192.168.1.9","wcc","fleisch","radiodj161")
#query = "SELECT title FROM history ORDER BY date_played DESC LIMIT 1"
query = "SELECT artist,title,song_type FROM songs WHERE NOT song_type=2 ORDER BY date_played DESC LIMIT 1;"
cur = db.cursor()
cur.execute(query)
row = cur.fetchone()
db.close()

if row != None:
    trackt = "Playing: " + row[0] + " - " + row[1]
    if row[2] != 0:
        trackt = ""
track = trackt[:60]

db = MySQLdb.connect("192.168.1.9","wcc","fleisch","radiodj161")
query = "SELECT songs.artist, songs.title FROM songs,queuelist WHERE songs.ID=queuelist.songID AND songs.song_type=0 LIMIT 1;"
cur = db.cursor()
cur.execute(query)
row = cur.fetchone()
db.close()

if row != None:
    ntrackt = row[0] + " - " + row[1]

ntrack = ntrackt[:60] + " "
#trackbarl = 46 - len(track)
#trackbar = "-" * trackbarl

def clear():
    return os.system('clear')

def inforow(title):
    titlen = len(title)
    titstart = "==="
    titend = "=" * (65 - titlen)
    titout = color.BOLD + titstart + " " + title + " " + titend + color.END
    print titout , "\n" + track + "\nNext Up: " + ntrack
#    print titout

def schedule(when):
    weekday = when.strftime("%a")
    daymon = when.strftime("%d%b")
    print "\n " + color.BOLD + weekday.upper() + "    " + daymon.upper() + "    PROGRAM" + color.END

def eventsbyday(when):
    global late
    global track
    schedule(when)
    day = int(when.strftime("%d"))
    lowlimit = day * 10000 + 800;
    highlimit = (day + 1) * 10000 + 306;
    db = MySQLdb.connect("localhost","root","radiowave","wcc")
    query = "SELECT * FROM radiolist WHERE id > " + str(lowlimit) + " and id < " + str(highlimit) + " ORDER BY id"
    cur = db.cursor()
    cur.execute(query)
    row = cur.fetchone()
    db.close()
    timebar = False
    pre = ""
    post = ""
    prevtime = ""
    while row is not None:
        time.sleep(0.1)
        eventdate = row[0][:2]

        if int(eventdate) != int(day):
            if late == False and timebar == False:
                pre = color.BOLD
                post = color.END
                eventtext = pre + eventtext + post
                timebar = True
                print("-" + nowtime + "-----------------------------------------------------------------")

            when2 = datetime.date(2015,9,int(eventdate))
            schedule(when2)
            day = eventdate
            if late == True:
                late = False

        eventtime = row[0][2:6]
        eventwhen = datetime.datetime(2015,9,int(eventdate),int(eventtime[:2]),int(eventtime[2:4]))
        nowwhen = datetime.datetime.fromtimestamp(time.time())
        nowtime = nowwhen.strftime("%H%M")
        eventustime = eventwhen.strftime("%I:%M%p")
        if eventustime[0] == "0":
            prettyustime = " " + eventustime.lstrip("0")
        else:
            prettyustime = eventustime
        eventtext = row[1]




        if int(nowtime) < int(eventtime) and timebar == False:
            if late == False:
                pre = color.BOLD
                post = color.END
                eventtext = pre + eventtext + post
                timebar = True
                print("-" + nowtime + "-----------------------------------------------------------------")

        print(" %s%s %s    %s%s") % (pre,str(eventtime),prettyustime,eventtext,post)


        pre = ""
        post = ""
        prevtime = str(eventtime)
        row = cur.fetchone()
    if timebar == False and prevtime != "":
        print("-" + nowtime + "-----------------------------------------------------------------")

clear()
inforow("SCHEDULE - WASTELAND RADIO 88.3 FM")
arg = 24
for argn in sys.argv:
    if argn.isdigit():
        arg = int(argn)

nowwhen = datetime.datetime.fromtimestamp(time.time())
thishour = int(nowwhen.strftime("%H"))
if thishour < 5:
    late = True
    arg = arg - 1
eventsbyday(datetime.date(2015,9,arg))
