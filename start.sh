#!/bin/sh

python manager.py & /usr/local/bin/gunicorn -b :$1 app:app