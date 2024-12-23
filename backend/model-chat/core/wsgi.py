import os
import eventlet.wsgi
import socketio
import eventlet

from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler

from core.socket import socket

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = StaticFilesHandler(get_wsgi_application())
application = socketio.WSGIApp(socket, application)

eventlet.wsgi.server(eventlet.listen(('', 8000)), application)