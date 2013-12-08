#!/bin/bash

BASENAME=$(dirname $0)
export PYTHONPATH=$BASENAME/tornado:$BASENAME/pika:$BASENAME/backend

python $BASENAME/backend/server.py
