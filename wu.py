#! /usr/bin/python
#--------------------
# WCC Utilities 0.0.8
# By Erik N8MJK
#--------------------

import time
import datetime
import curses
import traceback
import locale
import MySQLdb
import sys
import os
import pwd
import socket

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

subprogram = 0
curdate = ""
currtime = ""
updt_cnt1 = 0
updt_cnt2 = 0
db = None
user = pwd.getpwuid(os.getuid())[0]
operator = user.upper()
rloglist = ["callsign","rst_s","rst_r","qth","comments","timeoff","freq","power","band","mode","timeon","time","operator","location_id"]
ploglist = ["mailtype","internal","destcity","deststate","destzip","deststation","fromstation","barter","rdate"]

try:
    machine = socket.gethostname()
except:
    machine = "computer"

wccutil = "WCC Util 0.0.8"
msg_checktime = time.time()
message = 0

def xstr(s):
    if s is None:
        return ''
    return str(s)

def get_datetime():
    #let's make a pretty datetime
    global timeoutput
    t = datetime.datetime.now()
    currdatetime = t.timetuple()
    timeoutput = time.strftime("%d %b %Y %H:%M:%S",currdatetime)

def get_rcontacts(scope):
    global db
    if scope == "today":
        query = "SELECT callsign FROM rlog WHERE timeon BETWEEN SUBTIME(NOW(),'1 0:0:0') AND NOW();"
    if scope == "total":
        query = "SELECT callsign FROM rlog"
    try:
        db = MySQLdb.connect('localhost','wcc','radiowave','wcc')
        cur = db.cursor()
        cur.execute(query)
        rows = cur.rowcount
        return "%s" % rows
    except MySQLdb.Error, e:
        return "ERR"
    finally:
        if db:
            db.close()
    return "0"

def get_pcontacts(scope):
    global db
    if scope == "today":
        query = "SELECT id FROM post WHERE rdate BETWEEN SUBTIME(NOW(),'1 0:0:0') AND NOW();"
    if scope == "total":
        query = "SELECT id FROM post;"
    try:
        db = MySQLdb.connect('localhost','wcc','radiowave','wcc')
        cur = db.cursor()
        cur.execute(query)
        rows = cur.rowcount
        return "%s" % rows
    except MySQLdb.Error, e:
        return "ERR"
    finally:
        if db:
            db.close()
    return "0"

def heartbeat(operator,machine):
    global db
    query = "REPLACE INTO user_hb SET user='" + operator + "',machine='" + machine + "';"
    try:
        db = MySQLdb.connect('localhost','wcc','radiowave','wcc')
        cur = db.cursor()
        cur.execute(query)
        db.commit()
    except MySQLdb.Error, e:
        db.rollback()
        return "ERR"
    finally:
        if db:
            db.close()

def rlogtemp(input,field):
    global db
    global operator
    global machine
    global rloglist
    query = "INSERT INTO temp_rlog (%s,user,machine) VALUES ('%s','%s','%s') ON DUPLICATE KEY UPDATE %s='%s', user='%s', machine='%s';" % (rloglist[field],MySQLdb.escape_string(input),user.upper(),machine,rloglist[field],MySQLdb.escape_string(input),user.upper(),machine)
    try:
        db = MySQLdb.connect('localhost','wcc','radiowave','wcc')
        cur = db.cursor()
        cur.execute(query)
        db.commit()
    except MySQLdb.Error, e:
        db.rollback()
        return "ERR"
    finally:
        if db:
            db.close()
        return()

def plogtemp(input,field):
    global db
    global operator
    global machine
    global rloglist
    query = "INSERT INTO temp_post (%s,user,machine) VALUES ('%s','%s','%s') ON DUPLICATE KEY UPDATE %s='%s', user='%s', machine='%s';" % (MySQLdb.escape_string(ploglist[field]),MySQLdb.escape_string(str(input)),user.upper(),machine,MySQLdb.escape_string(ploglist[field]), MySQLdb.escape_string(str(input)),user.upper(),machine)
    try:
        db = MySQLdb.connect('localhost','wcc','radiowave','wcc')
        cur = db.cursor()
        cur.execute(query)
        db.commit()
    except MySQLdb.Error, e:
        db.rollback()
        return "ERR"
    finally:
        if db:
            db.close()
        return()

def message_input(rcpt,operator,machine,message):
    global db
    query = "INSERT INTO msgs SET sender='%s @ %s', rcpt='%s', body='%s';" % (MySQLdb.escape_string(operator), MySQLdb.escape_string(machine), MySQLdb.escape_string(rcpt), MySQLdb.escape_string(message))
    try:
        db = MySQLdb.connect('localhost','wcc','radiowave','wcc')
        cur = db.cursor()
        cur.execute(query)
        db.commit()
    except MySQLdb.Error, e:
        db.rollback()
        return "ERR"
    finally:
        if db:
            db.close()

def write_datetime(win):
    #separate function since this gets done A LOT
    get_datetime()

    win.move(0,59)
    win.clrtoeol()
    win.addstr(timeoutput, curses.A_REVERSE)
    win.refresh()

def write_rcontacts(win):
    win.addstr(2,17,get_rcontacts("total"))
    win.addstr(3,17,get_rcontacts("today"))
    win.refresh()

def write_pcontacts(win):
    win.addstr(2,17,get_pcontacts("total"))
    win.addstr(3,17,get_pcontacts("today"))
    win.refresh()

def check_messages(win):
    global operator
    global machine
    heartbeat(operator,machine)
    global db
    query = "SELECT * FROM msgs WHERE (rcpt = '" + operator + "' OR rcpt = '" + machine + "') AND (timestamp BETWEEN SUBTIME(NOW(),'0 0:0:15') AND NOW()) ORDER BY timestamp LIMIT 1;"
    try:
        db = MySQLdb.connect('localhost','wcc','radiowave','wcc')
        cur = db.cursor()
        cur.execute(query)
        rows = cur.rowcount
        message = rows
    except MySQLdb.Error, e:
        return "ERR"
    finally:
        if db:
            db.close()
    msg_checktime = time.time()
    if message > 0:
        win.addstr(23,1,"*** INCOMING MESSAGE***", curses.A_BLINK)
    win.refresh()

def get_oldinput(field):
    global operator
    global machine
    global db
    output = ""
    query = "SELECT %s FROM temp_rlog WHERE (user = '%s' AND machine = '%s') LIMIT 1;" % (field,operator,machine)
    try:
        db = MySQLdb.connect('localhost','wcc','radiowave','wcc')
        cur = db.cursor()
        cur.execute(query)
        row = cur.fetchone()
        if row[0] == None:
            output = ""
        else:
            output = row[0]
    except MySQLdb.Error, e:
        return "ERR"
    finally:
        if db:
            db.close()
    return(str(output))
    win.refresh()

def get_oldpost(field):
    global operator
    global machine
    global db
    output = ""
    query = "SELECT %s FROM temp_post WHERE (user = '%s' AND machine = '%s') LIMIT 1;" % (field,operator,machine)
    try:
        db = MySQLdb.connect('localhost','wcc','radiowave','wcc')
        cur = db.cursor()
        cur.execute(query)
        row = cur.fetchone()
        try:
            output = row[0]
            exit(output)
        except:
            pass
        else:
            output = ""
    except MySQLdb.Error, e:
        return "ERR"
    finally:
        if db:
            db.close()
    return(output)
    win.refresh()

def check_dupe(win,dupe):
    global db
    if len(dupe.strip(' ')) < 1:
        win.addstr(6,1," " * 25)
        win.addstr(9,1," " * 50)
        return
    query = "SELECT * FROM rlog WHERE callsign LIKE '%" + dupe + "%' ORDER BY timeon DESC LIMIT 1;"
    try:
        db = MySQLdb.connect('localhost','wcc','radiowave','wcc')
        cur = db.cursor()
        cur.execute(query)
        rows = cur.rowcount
    except MySQLdb.Error, e:
        return "ERR"
    finally:
        if db:
            db.close()
        win.addstr(6,1," " * 25)
        win.addstr(9,1," " * 50)
    if rows > 0:
        row = cur.fetchone()
        while row != None:
            if row[5] == None:
                t = datetime.datetime.now()
            else:
                t = row[5]
            msgdatetime = t.timetuple()
            yr = str(msgdatetime[0])
            msgdate = "%02d"%msgdatetime[2] + "/" + "%02d"%msgdatetime[1] + "/" + "%02d"%int(yr[2:])
            msgtime = "%02d:"%msgdatetime[3] + "%02d:"%msgdatetime[4] + "%02d"%msgdatetime[5]
            callsign = row[4]
            when = msgtime + " on " + msgdate
            mode = row[7]
            band = row[8]
            win.addstr(6,1,"Duplicate entry?",curses.A_BLINK)
            win.addstr(9,1,"%s at %s (%s,%s)" % (callsign,when,band,mode))
            break
    win.refresh()

def write_online(win):
    global db
    global operator
    global machine
    usercount = 0
    ei = 0
    heartbeat(operator,machine)
    query = "SELECT * FROM user_hb WHERE (timestamp BETWEEN SUBTIME(NOW(),'0 0:0:15') AND NOW()) ORDER BY user;"
    while ei < 8:
        win.move(4 + ei,61)
        win.clrtoeol()
        ei = ei + 1
    try:
        db = MySQLdb.connect('localhost','wcc','radiowave','wcc')
        cur = db.cursor()
        cur.execute(query)
        row = cur.fetchone()
        while row != None:
            thisuser = row[0]
            thismach = row[1]
            win.move(4 + usercount,61)
            win.addstr(thisuser[:9],curses.A_BOLD)
            win.addstr(" (" + thismach[:6] + ")")
            win.refresh()
            usercount = usercount + 1
            row = cur.fetchone()
    except MySQLdb.Error, e:
        return "ERR"
    finally:
        if db:
            db.close()

def write_messages(win):
    global operator
    global machine
    global db
    emptyline = " " * 59
    msgline = 4
    query = "SELECT * FROM (SELECT * FROM msgs ORDER BY timestamp DESC LIMIT 7) AS last ORDER BY last.timestamp ASC;"
    try:
        db = MySQLdb.connect('localhost','wcc','radiowave','wcc')
        cur = db.cursor()
        result = cur.execute(query)
        row = cur.fetchone()
        while row != None:
            t = row[4]
            msgdatetime = t.timetuple()
            yr = str(msgdatetime[0])
            msgdate = "%02d"%msgdatetime[2] + "/" + "%02d"%msgdatetime[1] + "/" + "%02d"%int(yr[2:])
            msgtime = "%02d:"%msgdatetime[3] + "%02d:"%msgdatetime[4] + "%02d"%msgdatetime[5]
            win.move(msgline,1)
            win.addstr(emptyline)
            win.move(msgline,1)
            win.addstr(row[1] + " says to " + row[2] + " (" + msgdate + " " + msgtime + ")")
            msgline = msgline + 1
            win.move(msgline,1)
            win.addstr(emptyline)
            win.move(msgline,1)
            win.addstr(row[3],curses.A_BOLD)
            msgline = msgline + 1
            win.refresh()
            row = cur.fetchone()
    except MySQLdb.Error, e:
        return "ERR"
    finally:
        if db:
            db.close()
    win.refresh()

def minimenu(win):
    global subprogram
    subwin = win.subwin(10,28,5,10)
    subwin.bkgd(" ", curses.A_REVERSE + curses.color_pair(1))
    subwin.nodelay(1)
    subwin.erase()
#    subwin.border("|","|","^","_","'","'",".",",")
    subwin.refresh()
    subwin.addstr(1,0,"---Menu---------------------")
    subwin.addstr(3,2,"1) Radio Log")
    subwin.addstr(4,2,"2) Radiogram Input")
    subwin.addstr(5,2,"3) Postal Log")
    subwin.addstr(6,2,"4) Messaging")
    subwin.addstr(7,2,"5) Operator")
    subwin.addstr(8,2,"6) Main Menu")
    subwin.refresh()
    while 1:
        inch = subwin.getch()
        if inch != -1:
            try:
                instr = chr(inch)
            except:
                pass
            else:
                if int(instr) == subprogram:
                    time.sleep(0.2)
                    return subwin
                if instr == '6':
                    subprogram = 0
                    return subwin
                subprogram = int(instr)
                return subwin

def init_window(win):
    win.erase()
    topstring = wccutil
    bottomstring = operator + " @ " + machine
    bottomfillstring = (78 - len(bottomstring)) * " "
    topfillstring = (78 - len(topstring)) * " "
    win.addstr(0,0," " + topstring + topfillstring, curses.A_REVERSE)
    win.addstr(23,0,bottomfillstring + bottomstring + " ", curses.A_REVERSE)


def draw_menu_window(win):
    init_window(win)
    win.addstr(2,1,"Main Menu",curses.A_BOLD)
    win.addstr(4,1,"1) Radio Communication Log")
    win.addstr(6,1,"2) Radio Telegram Input")
    win.addstr(8,1,"3) Postal Log")
    win.addstr(10,1,"4) Messaging")
    win.addstr(12,1,"5) Change Operator")
    win.addstr(14,1,"6) Exit")
    write_datetime(win)
    win.refresh()    
    menuloop(win)

def draw_message_window(win):
    global message
    init_window(win)
    message = 0
    vline = 0
    win.addstr(2,1,"Messaging", curses.A_BOLD)
    win.addstr(2,61,"Who's Online?", curses.A_BOLD)
    while vline < 18:
        win.move(vline + 1,60)
        win.addstr("|")
        vline = vline + 1
    senderstring = operator + " @ " + machine
    inputstring = " Send Message"
    inputfill = " " * (79 - len(inputstring))
    win.addstr(19,0,inputstring + inputfill, curses.A_REVERSE)
    win.addstr(20,1,"Sending as: " + senderstring)
    win.addstr(21,1,"Sending to: ")
    win.addstr(" " * 16)
    win.addstr(22,1,"Message:    ")
    emptyinput = " " * 61
    win.addstr(emptyinput)
    write_datetime(win)
    win.refresh()    
    rcptloop(win)

def draw_operator_window(win):
    init_window(win)
    win.addstr(2,1,"Change Operator on machine " + machine, curses.A_BOLD)
    win.addstr(4,1,"Current Operator: " + operator)
    win.addstr(6,1,"Enter new Operator: ")
    win.addstr(6,21,"                ", curses.A_UNDERLINE)
    write_datetime(win)
    win.refresh()    
    operatorloop(win)

def draw_plog_window(win):
    init_window(win)
    win.addstr(2,1,"Total Mail: ")
    win.addstr(3,1,"Mail Today: ")
    win.addstr(5,1,"Type  : ")
    win.addstr(5,44,"INT/EXT: ")
    win.addstr(6,1,"D.City: ")
    win.addstr(6,44,"D.State: ")
    win.addstr(6,59,"D.ZIP: ")
    win.addstr(7,1,"D.WCC : ")
    win.addstr(7,44,"D.Grid: ")
    win.addstr(7,59,"Date: ")
    win.addstr(8,1,"Barter: ")
    win.addstr(21,1,"WCC Location ID: ")
    win.addstr(20,60,".-------. .-------.")
    win.addstr(21,60,"| CLEAR | | ENTER |")
    win.addstr(22,60,"'-------' '-------'")
    write_pcontacts(win)
    write_datetime(win)
    win.refresh()    
    plogloop(win)

def get_button(win,posy,posx,name):
    win.keypad(1)
    win.addstr(posy,posx,name,curses.A_REVERSE)
    while 1:
        inch = win.getch()
        if inch != -1:
            #first look for special usables
            if inch == 96:
                #local topleft
                minimenu(win)
                break
            if inch == 167:
                #PuTTY topleft
                minimenu(win)
                break
            if inch == 10 or inch == 32:
                #enter or space
                win.addstr(posy,posx,name)
                return(-6)
            if inch == 9 or inch == 260 or inch == 261 or inch == 259 or inch == 258:
                win.addstr(posy,posx,name)
                #tab or left or right or up or down
                if inch == 258:
                    #down
                    return(-5)
                elif inch == 259:
                    #up
                    return(-4)
                elif inch == 260:
                    #left
                    return(-2)
                elif inch == 261:
                    #right
                    return(-3)
                else:
                    return(-1)
            try:
                instr = str(chr(inch))
            except:
                pass
            else:
                pass
        write_datetime(win)
        win.refresh()

def get_postbool(win,posy,posx,tname,fname,field):
    win.keypad(1)
    postintext = 0
    tfstring = " (UP or DOWN to change)"
    tf = get_oldpost(ploglist[field])
    tflist = [fname,tname]
    try:
        win.addstr(posy,posx,tflist[tf],curses.A_REVERSE)
    except:
        tf = 1
        win.addstr(posy,posx,tflist[tf],curses.A_REVERSE)
    win.addstr(posy,posx+3,tfstring)
    output = 0
    while 1:
        inch = win.getch()
        if inch != -1:
            #first look for special usables
            if inch == 96:
                #local topleft
                minimenu(win)
                break
            if inch == 167:
                #PuTTY topleft
                minimenu(win)
                break
            if inch == 259 or inch == 258:
                tf = tf + 1
                if tf == 2:
                    tf = 0
                win.addstr(posy,posx,tflist[tf],curses.A_REVERSE)
            if inch == 9 or inch == 260 or inch == 261:
                #tab or left or right or up or down
                postintext = tf
                plogtemp(tf,field)
                win.addstr(posy,posx,tflist[tf])
                win.addstr(" " * len(tfstring))
                if inch == 260:
                    #left
                    return(-2,postintext)
                elif inch == 261:
                    #right
                    return(-3,postintext)
                else:
                    return(-1,postintext)
        write_datetime(win)
        win.refresh()

def get_callinput(win,posy,posx,length,field):
    global rloglist
    win.keypad(1)
    starti = posy
    i = 0
    output = ""
    oldinput = get_oldinput(rloglist[field])
    if len(oldinput) > 0:
        i = len(oldinput)
        input_spaces = length - len(oldinput)
        emptyinput = oldinput + " " * input_spaces
    else:
        emptyinput = " " * length
    inputlist = list(emptyinput)
    win.addstr(posy,posx,emptyinput,curses.A_REVERSE)
    win.move(posy,posx+i)
    while 1:
        inch = win.getch()
        if inch != -1:
            #first look for special usables
            if inch == 96:
                #local topleft
                minimenu(win)
                break
                #PuTTY topleft
                minimenu(win)
                break
            if inch == 263 or inch == 8:
                if i > 0:
                    #backspace
                    i = i - 1
                    win.addstr(posy,posx + i," ",curses.A_REVERSE)
                    inputlist[i] = " "
                    dupecheck = ''.join(inputlist)                    
                    check_dupe(win,dupecheck.strip(' '))
                    win.move(posy,posx + i)
                    win.refresh()
            if inch == 9 or inch == 260 or inch == 261 or inch == 259 or inch == 258:
                #tab or left
                inputstring = "".join(inputlist)
                output = inputstring.strip(' ')
                win.addstr(posy,posx," " * length)
                win.addstr(posy,posx,output)
                rlogtemp(output,field)
                win.refresh()
                if inch == 258:
                    #down
                    return(-5)
                elif inch == 259:
                    #up
                    return(-4)
                elif inch == 260:
                    #left
                    return(-2)
                elif inch == 261:
                    #right
                    return(-3)
                else:
                    return(-1)
            try:
                instr = str(chr(inch))
            except:
                pass
            else:
                if inch < 128 and inch > 31 and i < length:
                    win.addstr(posy,posx + i,instr,curses.A_REVERSE)
                    inputlist[i] = "%s" % instr
                    dupecheck = ''.join(inputlist)                    
                    check_dupe(win,dupecheck.strip(' '))
                    i = i + 1
                    win.refresh()
                pass
        write_datetime(win)
        win.refresh()

def get_input(win,posy,posx,length,field):
    global rloglist
    win.keypad(1)
    starti = posy
    i = 0
    output = ""
    oldinput = get_oldinput(rloglist[field])
    if len(oldinput) > 0:
        input_spaces = length - len(oldinput)
        emptyinput = oldinput + " " * input_spaces
        i = len(oldinput)
    else:
        emptyinput = " " * length
    inputlist = list(emptyinput)
    win.addstr(posy,posx,emptyinput,curses.A_REVERSE)
    while 1:
        inch = win.getch()
        if inch != -1:
            #first look for special usables
            if inch == 96:
                #local topleft
                minimenu(win)
                break
            if inch == 167:
                #PuTTY topleft
                minimenu(win)
                break
            if inch == 263 or inch == 8:
                if i > 0:
                    #backspace
                    i = i - 1
                    inputlist[i] = " "
                    win.addstr(posy,posx + i," ",curses.A_REVERSE)
                    win.move(posy,posx + i)
                    win.refresh()
            if inch == 9 or inch == 260 or inch == 261 or inch == 259 or inch == 258:
                #tab or left
                inputstring = "".join(inputlist)
                output = inputstring.strip(' ')
                win.addstr(posy,posx," " * length)
                win.addstr(posy,posx,output)
                if len(output) > 0:
                    if field == 7:
                        win.addstr("W")
                    rlogtemp(output,field)
                win.refresh()
                if inch == 258:
                    #down
                    return(-5)
                elif inch == 259:
                    #up
                    return(-4)
                elif inch == 260:
                    #left
                    return(-2)
                elif inch == 261:
                    #right
                    return(-3)
                else:
                    return(-1)
            try:
                instr = str(chr(inch))
            except:
                pass
            else:
                if inch < 128 and inch > 31 and i < length:
                    win.addstr(posy,posx + i,instr,curses.A_REVERSE)
                    inputlist[i] = "%s" % instr
                    i = i + 1
                    win.refresh()
                pass
        write_datetime(win)
        win.refresh()

def get_postinput(win,posy,posx,length,field):
    global ploglist
    win.keypad(1)
    starti = posy
    i = 0
    output = ""
    oldinput = get_oldpost(ploglist[field])
    if len(oldinput) > 0:
        input_spaces = length - len(oldinput)
        emptyinput = oldinput + " " * input_spaces
    else:
        emptyinput = " " * length
    inputlist = list(emptyinput)
    win.addstr(posy, posx, emptyinput,curses.A_REVERSE)
    while 1:
        inch = win.getch()
        if inch != -1:
            #first look for special usables
            if inch == 96:
                #local topleft
                minimenu(win)
                break
            if inch == 167:
                #PuTTY topleft
                minimenu(win)
                break
            if inch == 263 or inch == 8 and i > 0:
                #backspace
                i = i - 1
                win.addstr(posy,posx + i," ",curses.A_REVERSE)
                win.move(posy,posx + i)
                win.refresh()
            if inch == 9 or inch == 260 or inch == 261 or inch == 259 or inch == 258:
                #tab or left
                inputstring = "".join(inputlist)
                output = inputstring.strip(' ')
                win.addstr(posy,posx," " * length)
                win.addstr(posy,posx,output)
                plogtemp(output,field)
                win.refresh()
                if inch == 258:
                    #down
                    return(-5)
                elif inch == 259:
                    #up
                    return(-4)
                elif inch == 260:
                    #left
                    return(-2)
                elif inch == 261:
                    #right
                    return(-3)
                else:
                    return(-1)
            try:
                instr = str(chr(inch))
            except:
                pass
            else:
                if inch < 128 and inch > 31 and i < length:
                    win.addstr(posy,posx + i,instr,curses.A_REVERSE)
                    inputlist[i] = "%s" % instr
                    i = i + 1
                    win.refresh()
                pass
        write_datetime(win)
        win.refresh()

def operatorloop(win):
    global operator
    i = 0;
    inputlist = list("                ")
    while 1:        
        inch = win.getch()
        if inch != -1:
            if inch == 263 or inch == 8:
                if i < 1:
                    break
                i = i - 1
                win.addstr(6,(i + 21)," ",curses.A_UNDERLINE)
                win.move(6,(i + 21))
                win.refresh()
            if inch == 10:
                inputstring = "".join(inputlist)
                output = inputstring.strip(' ')
                win.addstr(8,1,inputstring)
                win.refresh()
                operator = output
                break
            try:
                instr = str(chr(inch))
            except:
                pass
            else:
                if inch < 128 and inch > 31:
                    win.addstr(6,(i + 21),instr.upper())
                    i = i + 1
                    inputlist[i] = "%s" % instr.upper()
                    win.refresh()
                if inch == 9:
                    pass
                    #tab, change fields
                if inch == 96:
                    #local topleft
                    minimenu(win)
                    return()
                if inch == 167:
                    #PuTTY topleft
                    minimenu(win)
                    return()
	if time.time() > (msg_checktime + 10):
            check_messages(win)
        write_datetime(win)

def rcptloop(win):
    global operator
    win.keypad(1)
    starti = 12
    i = 1
    drawi = 0
    emptyinput = " " * 16
    inputlist = list(emptyinput)
    win.addstr(21,starti + i,emptyinput,curses.A_REVERSE)
    while 1:        
        inch = win.getch()
        if inch != -1:
            try:
                instr = str(chr(inch))
            except:
                pass
            else:
                if inch == 167:
                    #PuTTY topleft
                    minimenu(win)
                    return()
                if inch == 96:
                    #local topleft
                    minimenu(win)
                    return()
                if inch == 9:
                    break
                    #tab, change fields
                if inch == 263 or inch == 8:
                    if i + starti < starti + 2:
                        break
                    i = i - 1
                    win.addstr(21,starti + i," ",curses.A_REVERSE)
                    inputlist[i + 1] = " "
                    win.move(21,starti + i)
                    win.refresh()
                elif inch == 10:
                    inputstring = "".join(inputlist)
                    checkout = inputstring.strip(' ')
                    if len(checkout) > 1:
                        output = inputstring.strip()
                        win.addstr(21,starti + 1,output.upper() + " " * (len(emptyinput) - len(output)))
                        msgloop(win,output.upper())
                        break
                    else:
                        break
                elif i < 15:
                    win.addstr(21,starti + i,instr.upper())
                    i = i + 1
                    inputlist[i] = "%s" % instr
                    win.refresh()
        write_datetime(win)
        drawi = drawi + 1
        if drawi > 10:
            write_messages(win)
            write_online(win)
            drawi = 0
        win.move(21,starti + i)
        time.sleep(0.1)

def msgloop(win,rcpt):
    global operator
    win.keypad(1)
    i = 1
    starti = 12
    drawi = 0
    emptyinput = " " * 61
    inputlist = list(emptyinput)
    win.addstr(22,starti + i,emptyinput,curses.A_REVERSE)
    while 1:        
        inch = win.getch()
        if inch != -1:
            try:
                instr = str(chr(inch))
            except:
                pass
            else:
                if inch == 263 or inch == 8:
                    if i < 2:
                        break
                    i = i - 1
                    win.addstr(22,starti + i," ",curses.A_REVERSE)
                    win.move(22,starti + i)
                    win.refresh()
                elif inch == 10:
                    inputstring = "".join(inputlist)
                    output = inputstring.strip()
                    message_input(rcpt,operator,machine,output)
                    win.addstr(22,1,"Message:    ")
                    emptyinput = " " * 61
                    win.addstr(emptyinput,curses.A_UNDERLINE)
                    i = 1
                    win.refresh()
                    break
                elif i < 60:
                    win.addstr(22,starti + i,instr)
                    i = i + 1
                    inputlist[i] = "%s" % instr
                    win.refresh()
                if inch == 9:
                    pass
                    #tab, change fields
                if inch == 96:
                    #local topleft
                    minimenu(win)
                    return()
                if inch == 167:
                    #PuTTY topleft
                    minimenu(win)
                    return()
        write_datetime(win)
        drawi = drawi + 1
        if drawi > 10:
            write_messages(win)
            write_online(win)
            drawi = 0
        win.move(22,starti + i)
        time.sleep(0.1)

def draw_rlog_window(win):
    init_window(win)
    global operator
    global machine
    global db
    query = "SELECT * FROM temp_rlog WHERE (user = '%s' AND machine = '%s') LIMIT 1;" % (operator,machine)
    try:
        db = MySQLdb.connect('localhost','wcc','radiowave','wcc')
        cur = db.cursor()
        cur.execute(query)
        row = cur.fetchone()
    except MySQLdb.Error, e:
        return "ERR"
    finally:
        if db:
            db.close()
    win.addstr(2,1,"Total Contacts: ")
    win.addstr(3,1,"Contacts Today: ")
    win.addstr(5,1,"Callsign: " + xstr(row[4]))
    win.addstr(5,29,"RST Sent: " + xstr(row[10]))
    win.addstr(5,44,"RST Recd: " + xstr(row[11]))
    win.addstr(5,59,"Freq: " + xstr(row[6]))
    win.addstr(6,29,"Power: " + xstr(row[9]))
    if len(str(row[9])) > 0:
        win.addstr("W")
    win.addstr(6,44,"Band: " + xstr(row[8]))
    win.addstr(6,59,"Mode: " + xstr(row[7]))
    win.addstr(7,1,"QTH: " + xstr(row[13]))
    win.addstr(7,44,"D/T: " + xstr(row[5]))
    win.addstr(8,1,"Comments: " + xstr(row[14]))
    win.addstr(8,59,"TOff: " + xstr(row[12]))
    win.addstr(21,1,"WCC Location ID: " + xstr(row[3]))
    win.addstr(20,60,".-------. .-------.")
    win.addstr(21,60,"| CLEAR | | ENTER |")
    win.addstr(22,60,"'-------' '-------'")
    write_rcontacts(win)
    write_datetime(win)
    win.refresh()    
    rlogloop(win)

def plogloop(win):
    global subprogram
    global ploglist
    win.keypad(1)
    field = 0
    i = 0
    posy = 5
    posx = 11
    length = 16
    output = ""
    emptyinput = ""
    while 1:
        if field == 0:
            return_input = get_postinput(win,5,9,16,field)
            if return_input == -5:
                field = 2
            if return_input == -3:
                field = 1
            if return_input == -1:
                field = 1
        if field == 1:
            return_input = get_postbool(win,5,53,"INT","EXT",field)
            if return_input[0] == -5:
                field = 3
            if return_input[0] == -2:
                field = 0
            if return_input[0] == -1:
                if return_input[1] == 0:
                    field = 2
                else:
                    field = 5
        if field == 2:
            return_input = get_postinput(win,6,9,32,field)
            if return_input == -5:
                field = 5
            if return_input == -4:
                field = 0
            if return_input == -3:
                field = 3
            if return_input == -1:
                field = 3
        if field == 3:
            return_input = get_postinput(win,6,53,3,field)
            if return_input == -4:
                field = 1
            if return_input == -3:
                field = 4
            if return_input == -2:
                field = 2
            if return_input == -1:
                field = 4
        if field == 4:
            return_input = get_postinput(win,6,65,12,field)
            if return_input == -5:
                field = 8
            if return_input == -2:
                field = 3
            if return_input == -1:
                field = 7
        if field == 5:
            return_input = get_postinput(win,7,9,8,field)
            if return_input == -5:
                field = 7
            if return_input == -4:
                field = 2
            if return_input == -3:
                field = 8
            if return_input == -1:
                field = 7
        if field == 6:
            return_input = get_postinput(win,21,18,8,field)
            if return_input == -4:
                field = 7
            if return_input == -3:
                field = 9
            if return_input == -1:
                field = 9
        if field == 7:
            return_input = get_postinput(win,8,9,32,field)
            if return_input == -5:
                field = 6
            if return_input == -4:
                field = 5
            if return_input == -1:
                field = 9
        if field == 8:
            return_input = get_postinput(win,7,64,6,field)
            if return_input == -5:
                field = 9
            if return_input == -4:
                field = 4
            if return_input == -2:
                field = 5
            if return_input == -1:
                field = 6
        if field == 9:
            return_input = get_postinput(win,5,11,16,field)
            if return_input == -5:
                field = 2
            if return_input == -3:
                field = 1
            if return_input == -1:
                field = 1
        if field == 10:
            return_input = get_postinput(win,5,11,16,field)
            if return_input == -5:
                field = 2
            if return_input == -3:
                field = 1
            if return_input == -1:
                field = 1
        if field == 11:
            return_input = get_postinput(win,5,11,16,field)
            if return_input == -5:
                field = 2
            if return_input == -3:
                field = 1
            if return_input == -1:
                field = 1
	if time.time() > (msg_checktime + 10):
            check_messages(win)
        write_datetime(win)

def rlogloop(win):
    global subprogram
    global rloglist
    win.keypad(1)
    field = 0
    i = 0
    posy = 5
    posx = 11
    length = 16
    output = ""
    emptyinput = ""
    while 1:
        if field == 1: #RST Sent
            return_input = get_input(win,5,39,3,field)
            if return_input == -5:
                field = 7
            if return_input == -3:
                field = 2
            if return_input == -2:
                field = 0
            if return_input == -1:
                field = 2
        if field == 2: #RST Rec'd
            return_input = get_input(win,5,54,3,field)
            if return_input == -5:
                field = 8
            if return_input == -3:
                field = 6
            if return_input == -2:
                field = 1
            if return_input == -1:
                field = 3
        if field == 3: #QTH
            return_input = get_input(win,7,6,36,field)
            if return_input == -5:
                field = 4
            if return_input == -4:
                field = 0
            if return_input == -3:
                field = 10
            if return_input == -1:
                field = 4
        if field == 4: #Comments
            return_input = get_input(win,8,11,47,field)
            if return_input == -5:
                field = 13
            if return_input == -4:
                field = 3
            if return_input == -3:
                field = 5
            if return_input == -1:
                field = 5
        if field == 5: #Time Off
            return_input = get_input(win,8,65,4,field)
            if return_input == -5:
                field = 14
            if return_input == -4:
                field = 9
            if return_input == -2:
                field = 4
            if return_input == -1:
                field = 6
        if field == 6: #Freq
            return_input = get_input(win,5,65,8,field)
            if return_input == -5:
                field = 9
            if return_input == -2:
                field = 2
            if return_input == -1:
                field = 7
        if field == 7: #Power
            return_input = get_input(win,6,36,5,field)
            if return_input == -5:
                field = 3
            if return_input == -4:
                field = 1
            if return_input == -3:
                field = 8
            if return_input == -1:
                field = 8
        if field == 8: #Band
            return_input = get_input(win,6,50,6,field)
            if return_input == -5:
                field = 10
            if return_input == -4:
                field = 2
            if return_input == -3:
                field = 9
            if return_input == -2:
                field = 7
            if return_input == -1:
                field = 9
        if field == 9: #Mode
            return_input = get_input(win,6,65,6,field)
            if return_input == -5:
                field = 5
            if return_input == -4:
                field = 6
            if return_input == -2:
                field = 8
            if return_input == -1:
                field = 10
        if field == 10: #Date/Time
            return_input = get_input(win,7,49,19,field)
            if return_input == -4:
                field = 8
            if return_input == -2:
                field = 3
            if return_input == -1:
                field = 13
        if field == 13: #WCC Location ID
            return_input = get_input(win,21,18,8,field)
            if return_input == -4:
                field = 4
            if return_input == -3:
                field = 14
            if return_input == -1:
                field = 15
        if field == 14:
            return_input = get_button(win,21,62,"CLEAR")
            if return_input == -6:
                pass #clear all fields and reset temp_rlog values
            if return_input == -4:
                field = 5
            if return_input == -3:
                field = 15
            if return_input == -2:
                field = 12
            if return_input == -1:
                field = 0
        if field == 15:
            return_input = get_button(win,21,72,"ENTER")
            if return_input == -6:
                pass #complete rlog sequence
            if return_input == -4:
                field = 5
            if return_input == -2:
                field = 14
            if return_input == -1:
                field = 14
        if field == 0:
            return_input = get_callinput(win,posy,posx,16,field)
            if return_input == -5:
                field = 3
            if return_input == -3:
                field = 1
            if return_input == -1:
                field = 1
	if time.time() > (msg_checktime + 10):
            check_messages(win)
        write_datetime(win)

def menuloop(win):
    global subprogram
    while 1:
        inch = win.getch()
        if inch != -1:
            win.addstr(1,1,"     ")
            win.addstr(1,1,str(inch))
            try:
                instr = str(chr(inch))
            except:
                pass
            else:
                if inch == 9:
                    pass
                    #tab, change fields
                if inch == 96:
                    #local topleft
                    break
                if inch == 167:
                    #PuTTY topleft
                    break
                if instr == '1':
                    subprogram = 1
                    break
                if instr == '3':
                    subprogram = 3
                    break
                if instr == '4':
                    subprogram = 4
                    break
                if instr == '5':
                    subprogram = 5
                    break
                if instr == '6':
                    subprogram = -1
                    break
	if time.time() > (msg_checktime + 10):
            check_messages(win)
        write_datetime(win)

def mainloop(win):
    global subprogram
    global operator
    global machine
    heartbeat(operator,machine)
    win.nodelay(1)
    while subprogram != -1:
        if subprogram == 0:
            draw_menu_window(win)
        if subprogram == 1:
            draw_rlog_window(win)
        if subprogram == 3:
            draw_plog_window(win)
        if subprogram == 4:
            draw_message_window(win)
        if subprogram == 5:
            draw_operator_window(win)

def startup():
    #wrapper to avoid console errors on program bug
    #totally stolen btw
    try:
        # Initialize curses
        stdscr = curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        stdscr.bkgd(curses.color_pair(1));

        # Turn off echoing of keys, and enter cbreak mode,
        # where no buffering is performed on keyboard input
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(1)

        mainloop(stdscr)                # Enter the main loop

        # Set everything back to normal
        curses.echo()
        curses.nocbreak()
        stdscr.keypad(0)

        curses.endwin()                 # Terminate curses
    except:
        # In event of error, restore terminal to sane state.
        curses.echo()
        curses.nocbreak()
        stdscr.keypad(0)
        curses.endwin()
        traceback.print_exc()           # Print the exception

if __name__=='__main__':
    startup()


