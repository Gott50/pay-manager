#!/bin/sh

python start.py & /usr/local/bin/gunicorn -b :$1 app:app