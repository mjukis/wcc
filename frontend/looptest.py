#! /usr/bin/python
#--------------------
# WasteComm Terminal
# v0.0.1
# By Erik N8MJK
#--------------------

import time
import datetime
import curses
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado import gen

def xstr(s):
    if s is None:
        return ''
    return str(s)

def draw_background(win):
    win.erase()
    topstring = "WASTECOMM NET TERMINAL"
    bottomstring = "WCC#657"
    bottomfillstring = (78 - len(bottomstring)) * " "
    topfillstring = (78 - len(topstring)) * " "
    win.addstr(0,0," " + topstring + topfillstring, curses.A_REVERSE)
    win.addstr(23,0,bottomfillstring + bottomstring + " ", curses.A_REVERSE)

def get_datetime():
    #let's make a pretty datetime
    global timeoutput
    global dateoutput
    t = datetime.datetime.now()
    currdatetime = t.timetuple()
    dateoutput = time.strftime("%Y-%m-%d",currdatetime)
    timeoutput = time.strftime("%d %b %Y %H:%M:%S",currdatetime)

def write_datetime(win):
    #let's write that pretty datetime
    get_datetime()
    win.move(0,59)
    win.clrtoeol()
    win.addstr(timeoutput, curses.A_REVERSE)
    win.move(0,0)
    win.refresh()

def task():
    #function that calls the datetime-writer
    write_datetime(stdscr)

def task2():
    #function that proves async by writing RAGH
    win = stdscr
    win.move(2,3)
    win.addstr("RAGH")

def task3():
    #function that kills the program cleanly after a set time
    #this needs to be replaced by an ending to a proper main loop
    #so unexpected interruptions are handled without fucking
    #the terminal
    win = stdscr
    stdscr.keypad(0)
    curses.echo()
    curses.nocbreak()
    curses.endwin()
    exit()

def task4():
    #function that reads and displays keypresses
    win = stdscr
    inch = win.getch()
    if inch > -1:
        win.move(3,3)
        win.addstr("      ")
        win.move(3,3)
        win.addstr(xstr(inch))

if __name__ == "__main__":
    try:
        # Initialize curses
        stdscr=curses.initscr()
        global stdscr
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        stdscr.bkgd(curses.color_pair(1))
        # Turn off echoing of keys, and enter cbreak mode,
        # where no buffering is performed on keyboard input
        curses.noecho()
        curses.cbreak()
        #next line makes getch() nonblocking
        stdscr.nodelay(1)
        # In keypad mode, escape sequences for special keys
        # (like the cursor keys) will be interpreted and
        # a special value like curses.KEY_LEFT will be returned
        stdscr.keypad(1)
    except:
        # In event of error, restore terminal to sane state.
        stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    draw_background(stdscr)
    #the following line is kinda shitty because it loops an
    #input grab even though the input grab is not blocking,
    #which sort of simulates a laggy keyboard but should be a
    #normal callback for menus maybe?
    PeriodicCallback(task4, 100).start()
    PeriodicCallback(task, 1000).start()
    PeriodicCallback(task2, 3000).start()
    PeriodicCallback(task3, 10000).start()
    IOLoop.instance().start()
