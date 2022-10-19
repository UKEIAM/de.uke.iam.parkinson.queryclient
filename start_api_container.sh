#!/bin/bash

/usr/sbin/sshd -D &
cd /data/src
/usr/local/bin/gunicorn -w 4 --bind 0.0.0.0:5000 gunicorn_access:app
