#!/bin/sh

gunicorn --bind 0.0.0.0:8003 --workers 4 "flask_app:flask_app()"