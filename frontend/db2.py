#! /usr/bin/python
#--------------------
# WasteComm Terminal
# Tornado IOStream
# By Erik N8MJK
#--------------------

import tornado.ioloop
import tornado.iostream
import socket

def send_request():
    stream.write("GET /wcc_msgs/_changes?feed=continuous HTTP/1.0\r\nHost: localhost:5984\r\n\r\n")
    stream.read_until_close(callback=changeclose,streaming_callback=changereader) 

def changeclose(feed):
    pass

def changereader(feed):
    print feed

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
stream = tornado.iostream.IOStream(s)
stream.connect(("localhost",5984),send_request)
tornado.ioloop.IOLoop.instance().start()
