#! /usr/bin/python
#--------------------
# WCC Utilities 0.0.7
#--------------------

class db:
	def __init__(self):
		# Set operator
		self.operator = pwd.getpwuid(os.getuid())[0].upper()
		# Set machine
		try:
		    self.machine = socket.gethostname()
		except:
		    self.machine = "computer"
		return

	def set_operator(op_name):
		self.operator=op_name

class mysql(db):
	import MySQLdb

	def __init__(self):
		db.__init__(self)
		host = 'localhost'
		login = 'wcc'
		password = 'secret'
		db = 'database'
		try:
			self.db_socket = MySQLdb.connect(host, login, pwd, db)
		except MySQLdb.Error, e:
			quit('MySQL ERROR')
		finally:
			return

	def __del__(self):
		self.db_socket.close()

	def __enter__(self):
		return self

	def __exit__(self, type, value, traceback):
		self.db_socket.close()

	def q(query_string):
		#run a query and return result 
		return

	def c(query_string):
		#run a query and return row count
		return

class local_test(db):
	def __init__(self):
		import sqlite3
		self.db_socket = sqlite3.connect(':memory:')

