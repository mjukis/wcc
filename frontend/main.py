#! /usr/bin/python
#--------------------
# WasteComm Terminal
# v0.0.3
# By Erik N8MJK
#--------------------

import time
import datetime
import curses
import curses.ascii
import signal
import sys
from tornado.ioloop import IOLoop, PeriodicCallback
import tornado.iostream
import socket

from mainmenu import *
from globs import *

global stdscr

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
    win.addstr(2,1,title_en,curses.A_BOLD)
    win.addstr(prompty,promptx,promptstr)
    line = 2
    for i in range(0, len(items_en)):
        line = line + 2
        win.addstr(line,1," > " + items_en[i])
def get_datetime():
    #let's make a pretty datetime
    global timeoutput
    global dateoutput
    t = datetime.datetime.now()
    currdatetime = t.timetuple()
    dateoutput = time.strftime("%Y-%m-%d",currdatetime)
    timeoutput = time.strftime("%d %b %H:%M:%S ",currdatetime)

def write_datetime(win):
    #let's write that pretty datetime
    global prompty
    global promptx
    global promptstr
    global promptlen
    global curx
    get_datetime()
    win.move(0,63)
    win.clrtoeol()
    win.addstr(timeoutput, curses.A_REVERSE)
    win.move(prompty,curx)
    win.refresh()

def task():
    #function that calls the datetime-writer
    write_datetime(stdscr)

def task2():
    win = stdscr
    win.move(23,1)
    win.addstr("                    ", curses.A_REVERSE)

def incoming(feed):
    win = stdscr
    win.move(23,1)
    win.addstr("* INCOMING MESSAGE *", curses.A_BLINK)
    ftime = time.time() + 30
    IOLoop.instance().add_timeout(ftime,task2)

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
    global curx
    global prompty
    global userinput
    global inputpos
    win = stdscr
    inch = win.getch()
    if inch > -1:
        #check for escape chars
        if inch == 167 or inch == 27:
	    task3()
        #check for enter
        if inch == 10:
            win.addstr(prompty-1,1,xstr(userinput))
        #check for backspace
        if inch == 263:
            inputpos = inputpos - 1
            userinput[inputpos] = " "
            win.addstr(prompty,curx-1," ")
            curx = curx - 1
            win.move(prompty,curx)
        #print printable chars on prompt line
        if curses.ascii.isprint(inch):
            win.addstr(prompty,curx,chr(inch))
            userinput.append(" ")
            userinput[inputpos] = chr(inch)
            inputpos = inputpos + 1
            curx = curx + 1
            win.move(prompty,curx)
        #show ASCII values of other stuffs
        else:
            win.addstr(20,15,xstr(inch))

def changefeed_closed(feed):
    pass

def request_changefeed():
    stream.write("GET /wcc_msgs/_changes?feed=continuous&timeout=60000&heartbeat=30000 HTTP/1.0\r\nHost: localhost:5984\r\n\r\n")
    stream.read_until_close(callback=changefeed_closed,streaming_callback=incoming)

def signal_term_handler(signal, frame):
    print 'got SIGTERM'
    curses.reset_shell_mode()
    sys.exit(0)

if __name__ == "__main__":
    try:
        # Initialize curses
        stdscr = curses.initscr()
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
    # PeriodicCallback(task3, 10000).start()
    def signal_term_handler(signal, frame):
      print 'got SIGINT, bailing\r\n'
      curses.reset_shell_mode()
      sys.exit(0)
    signal.signal(signal.SIGINT, signal_term_handler)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    stream = tornado.iostream.IOStream(s)
    stream.connect(("localhost",5984),request_changefeed)
    task2()
    IOLoop.instance().start()
