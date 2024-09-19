#!/bin/sh
. /venv/bin/activate
exec python /api_model_chat/manage.py runserver 0.0.0.0:8000
