from django.urls import re_path

from DiscoCodeClient.consumers import client

websocket_urlpatterns = [
    re_path(r'ws/client/$', client.ClientConsumer.as_asgi())
]