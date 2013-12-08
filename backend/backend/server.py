#!env python

import tornado.ioloop
import logging, sys, pika

class HostBackend():
	"""
	>>> ioloop = tornado.ioloop.IOLoop()
	>>> survur = HostBackend(ioloop)
	True
	"""

	def __init__(self, ioloop):
		self.ioloop = ioloop
		self.rabbitcredentials = pika.PlainCredentials('username', 'password')
		self.rabbitparams = pika.ConnectionParameters('localhost', 5672, '/', self.rabbitcredentials)
		self.pikaconn = pika.SelectConnection(self.rabbitparams, self.on_pika_connect)

	def on_pika_connect(self, connection):
		pass

if __name__ == "__main__":
    import doctest
    doctest.testmod()

