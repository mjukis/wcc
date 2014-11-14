#! /usr/bin/python
#--------------------
# WasteComm Terminal
# Global Variables
# By Erik N8MJK
#--------------------

#set variables
prompty = 22
promptx = 1
promptstr = "WCC#657:>"

#starting values for globals
userinput = []
inputpos = 0

#calculated variables
promptlen = len(promptstr) + 2
curx = promptlen

#global functions
def xstr(s):
    if s is None:
        return ''
    return str(s)


