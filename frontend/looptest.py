#! /usr/bin/python
#--------------------
# WCC Async Frontend
# v0.0.1
# By Erik N8MJK
#--------------------

import time
import datetime
import curses
from tornado.ioloop import IOLoop, PeriodicCallback

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
    #write the pretty datetime
    get_datetime()
    win.move(0,59)
    win.clrtoeol()
    win.addstr(timeoutput, curses.A_REVERSE)
    win.move(0,0)
    win.refresh()

def task():
    #write the topright clock
    write_datetime(stdscr)

def task2():
    #write a string on the screen
    win = stdscr
    win.move(2,3)
    win.addstr("RAGH")

def task3():
    #kill the application
    win = stdscr
    stdscr.keypad(0)
    curses.echo()
    curses.nocbreak()
    curses.endwin()
    exit()

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
        #traceback.print_exc()           # Print the exception
    draw_background(stdscr)
    PeriodicCallback(task, 1000).start()
    PeriodicCallback(task2, 3000).start()
    PeriodicCallback(task3, 10000).start()
    IOLoop.instance().start()

