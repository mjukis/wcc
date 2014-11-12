#! /usr/bin/python
#--------------------
# WasteComm Terminal
# Menu Page v0.0.1
# By Erik N8MJK
#--------------------

from tornado.ioloop import IOLoop
import couchdb
import trombi

def pchange(change):
    print change

def main():
    s = trombi.Server('http://localhost:5984')
    db = trombi.Database(s, 'wcc_msgs')
    db.changes(pchange, feed='continuous', heartbeat='1000')

if __name__ == '__main__':
    ioloop = IOLoop.instance()
    ioloop.add_callback(main)
    ioloop.start()
