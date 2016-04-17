#!/usr/bin/python

# WASTELAND EVENT INPUT
# By Erik N8MJK

import curses
import MySQLdb

stdscr = curses.initscr()
stdscr.keypad(1)

emptyline = " " * 60

def clearline(line):
  stdscr.addstr(line,0,emptyline)

done = "N"

while done.upper() == "N":
  stdscr.clear()
  stdscr.addstr(1,0,"Which date would you like to edit? ")
  day = int(stdscr.getstr(2))

  while day < 1 or day > 31:
    clearline(1)
    stdscr.addstr(1,0,"Please enter a valid date: ")
    day = int(stdscr.getstr(2))

  lowlimit = day * 100000000 + 7000000;
  highlimit = (day + 1) * 100000000 + 3010000;
  db = MySQLdb.connect("localhost","root","radiowave","wcc")
  query = "SELECT * FROM eventlist WHERE id > " + str(lowlimit) + " and id < " + str(highlimit) + " ORDER BY id"
  cur = db.cursor()
  cur.execute(query)
  row = cur.fetchone()
  db.close()
  i = 2
  clearline(1)
  stdscr.addstr(1,0,"ID         | Event")
  idlist = []
  desclist = []
  while row != None:
    idlist.append(row[0])
    desclist.append(row[1])
    clearline(i)
    stdscr.addstr(i,0,row[0] + " | " + row[1])
    row = cur.fetchone()
    i = i + 1

  i = i + 1

  id = -1
  while id < 0:
    clearline(i)
    stdscr.addstr(i,0,"Enter [A] to add, [C] to cancel, or ID to edit: ")
    selection = stdscr.getstr(10)
    if selection == "a" or selection == "A":
      i = i + 2
      stdscr.addstr(i,0,"New ID (DDHHMMCiii): ")
      hour = str(stdscr.getstr(10))
      i = i + 1
      stdscr.addstr(i,0,"Event Name: ")
      newevent = str(stdscr.getstr(45))
      idb = MySQLdb.connect("localhost","root","radiowave","wcc")
      insertquery = "INSERT INTO eventlist (id,name) VALUES ('" + str(hour) + "','" + newevent  + "')"
      icur = idb.cursor()
      icur.execute(insertquery)
      idb.commit()
      icur.close()
      idb.close()
      id = 0
    if selection.upper() == "C":
      id = 0
    if selection in idlist:
      id = idlist.index(selection)
      stdscr.clear()
      stdscr.addstr(1,0,"ID         | Event")
      stdscr.addstr(2,0,idlist[id] + " | " + desclist[id])
      stdscr.addstr(4,0,"Change [I]D, Change [E]vent, [D]elete ")
      choice = stdscr.getstr(1)
      newid = idlist[id]
      newname = desclist[id]
      if choice.upper() == "I":
        stdscr.addstr(6,0,"New ID (DDHHMMCiii): ")
        newid = str(stdscr.getstr(10))
      if choice.upper() == "E":
        stdscr.addstr(6,0,"New Event Name: ")
        newname = str(stdscr.getstr(45))
      if choice.upper() != "D":
        updatequery = "UPDATE eventlist SET id = '" + newid + "',name='" + newname + "' WHERE id = '" + idlist[id] + "'"
      else:
        updatequery = "DELETE FROM eventlist WHERE id = '" + idlist[id]  + "'"

      udb = MySQLdb.connect("localhost","root","radiowave","wcc")
      ucur = udb.cursor()
      ucur.execute(updatequery)
      udb.commit()
      ucur.close()
      udb.close()
      
  stdscr.clear()
  stdscr.addstr(1,0,"Done? (Y/N)")
  done = stdscr.getstr(1)

stdscr.keypad(0)
curses.endwin()
