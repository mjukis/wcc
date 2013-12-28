#!/usr/bin/python

from passlib.apps import custom_app_context as pwd_context
import httplib2
import couchdb
import logging
from p import createpwd

logging.basicConfig(level=logging.DEBUG)
try:
    couch = couchdb.Server('http://wastecomm.net:5984')
    userdb = couch['wccusers']
    pwddb = couch['wccpwd']
except:
    print "Database fault!"

def makehash(word):
#takes the desired salted password and returns a hash
    try:
        hash = pwd_context.encrypt(word)
    except:
        print "Hashing failure!"
    else:
        return hash

def getuserid(user):
#takes username and tries to fetch the proper wccid from the db
    try:
        for row in userdb.view('wccids/by_username', None, key=str(user)):
            info = userdb.get(row.id)
        userid = info['wccid']
    except:
        print "Database fault!"
    else:
        return userid

def getpwddoc(user):
#attempts to return doc for user in password db
    try:
        for row in pwddb.view('wccpwd/by_username', None, key=str(user)):
            info = pwddb.get(row.id)
    except:
        print "No such user!"
    else:
        return info

def storepwd(user,pwd):
#attempts to take username and password and store the desired
#password in the database
    try:
        doc = getpwddoc(user)
        doc['word'] = makehash(createpwd(user,pwd))
        pwddb.save(doc)
    except:
        print "Password storage failure!"

def checkpwd(user,pwd):
#attempts to verify the password against the username
    try:
        doc = getpwddoc(user)
        storedhash = doc['word']
        inputpwd = createpwd(user,pwd)
        result = pwd_context.verify(inputpwd, storedhash)
    except:
        return False
    else:
        return result

def usernames():
#attempts to fetch list of usernames and return it
    userlist = list()
    try:
        view = userdb.view('wccids/usernames', None)
        for username in view:
            userlist.append(username.value)
    except:
        print "Failed to fetch userlist"
    else:
        return userlist

def userids():
#attempts to fetch list of userids and return it
    userlist = list()
    try:
        view = userdb.view('wccids/wccids', None)
        for userid in view:
            userlist.append(userid.value)
    except:
        print "Failed to fetch userlist"
    else:
        return userlist

def callsigns():
#attempts to fetch list of userids and return it
    userlist = list()
    try:
        view = userdb.view('wccids/callsigns', None)
        for callsign in view:
            userlist.append(callsign.value)
    except:
        print "Failed to fetch userlist"
    else:
        return userlist

def dupeusername(user):
#returns whether username exists in database
    names = usernames()
    for username in names:
        if user == username:
            return True
    return False

def dupewccid(id):
#returns whether wccid exists in database
    ids = userids()
    for userid in ids:
        if str(id) == str(userid):
            return True
    return False

def dupecallsign(callsign):
#returns whether callsign exists in database
    signs = callsigns()
    for sign in signs:
        if callsign == sign:
            return True
    return False

def createuser(wccid,firstname,nickname,username,callsign):
#attempts to create a new user in database
#first check if wccid is taken
    if dupewccid(wccid):
        print "Duplicate WCC ID!"
        return False
#next check if username is taken
    if dupeusername(username):
        print "Duplicate username!"
        return False
#last check if callsign is taken
    if dupecallsign(callsign):
        print "Duplicate callsign!"
        return False
#make user in userdb
    try:
        newdoc = {'wccid': str(wccid), 'firstname': firstname, 'nickname': nickname, 'username': username, 'callsign': callsign} 
        userdb.save(newdoc)
    except:
        print "Failed to make user in userdb!"
        return False
#make user in pwddb
    try:
        newdoc = {'userid': username, 'word': ''}
        pwddb.save(newdoc)
    except:
        print "Failed to make user in pwddb!"
        return False
    return True

#createuser("11801","Adam","Kasper","kasper","KJ6TAH")
#print usernames()
#storepwd("kasper","radiowave")
print(checkpwd("kasper","radiowave"))
