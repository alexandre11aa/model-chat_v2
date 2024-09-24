#!/bin/sh
. /venv/bin/activate
exec python /model_chat/manage.py runserver 0.0.0.0:8000
