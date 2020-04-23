#!/bin/bash

service nginx start
cd backend
gunicorn --bind 0.0.0.0:8000 --workers 4 --timeout 60 --log-level DEBUG -k gevent wsgi:application