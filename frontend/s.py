#! /usr/bin/python
#--------------------
# WasteComm Terminal
# CouchDB msgs send
# By Erik N8MJK
#--------------------

import sys
import couchdb

couch = couchdb.Server('http://localhost:5984')
db = couch['wcc_msgs']

args = []
i = 0
for arg in sys.argv:
    if i > 0:
        args.append(arg)
    i = i + 1

body = ' '.join(args)

doc = {'from':'swede','src':'wcc657','body':body}
db.save(doc)
