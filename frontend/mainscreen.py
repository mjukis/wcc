#! /usr/bin/python
#--------------------
# WasteComm Terminal
# v0.0.1
# By Erik N8MJK
#--------------------

import time
import datetime
import curses
import curses.ascii
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado import gen
from mainmenu import *
import psutil

prompty = 22
promptx = 1
promptstr = "WCC#657:>"
promptlen = len(promptstr) + 2
curx = promptlen
userinput = []
inputpos = 0

def xstr(s):
    if s is None:
        return ''
    return str(s)

def draw_background(win):
    global prompty
    global promptx
    global promptstr
    win.erase()
    topstring = "WASTECOMM NET TERMINAL"
    bottomstring = "WCC#657"
    bottomfillstring = (78 - len(bottomstring)) * " "
    topfillstring = (78 - len(topstring)) * " "
    win.addstr(0,0," " + topstring + topfillstring, curses.A_REVERSE)
    win.addstr(23,0,bottomfillstring + bottomstring + " ", curses.A_REVERSE)
    win.addstr(1,1,"     CPU:")
    win.addstr(2,1,"MEM.VIRT:") 
    win.addstr(3,1,"MEM.SWAP:") 

    win.addstr(1,25,"C1 VOLTS:")
    win.addstr(2,25," C1 AMPS:") 
    win.addstr(3,25,"C2 VOLTS:")
    win.addstr(4,25," C2 AMPS:") 
    win.addstr(5,25," kWh DAY:")

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
    global prompty
    global promptx
    global promptstr
    global promptlen
    global curx
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
    win.addstr(1,11,"      ")
    win.addstr(1,11,xstr("%05.1f"%psutil.cpu_percent()) + "%")
    virt = psutil.virtual_memory()
    win.addstr(2,11,"      ")
    win.addstr(2,11,xstr("%05.1f"%virt[2]) + "%")
    swap = psutil.swap_memory()
    win.addstr(3,11,"      ")
    win.addstr(3,11,xstr("%05.1f"%swap[3]) + "%")

    v1 = 120.6
    v2 = 119.9
    i1 = 9.9
    i2 = 2.6
    win.addstr(1,39,"     ")
    win.addstr(1,39,xstr("%05.1f"%v1))
    win.addstr(2,39,"     ")
    win.addstr(2,40,xstr("%04.1f"%i1))
    win.addstr(3,39,"     ")
    win.addstr(3,39,xstr("%05.1f"%v2))
    win.addstr(4,39,"     ")
    win.addstr(4,40,xstr("%04.1f"%i2))
    
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
        #check for escape chars
        if inch == 167 or inch == 27:
	    task3()

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
    PeriodicCallback(task2,2000).start()
#    PeriodicCallback(task3, 10000).start()
    IOLoop.instance().start()
