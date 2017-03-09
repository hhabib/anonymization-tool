#!/bin/bash

service nginx restart

cd /code/
#uwsgi --ini /code/flaskapp_uwsgi.ini
python server.py
