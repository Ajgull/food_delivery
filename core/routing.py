from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/support/$', consumers.SupportConsumer.as_asgi()),
    re_path(r'ws/order_countdown/$', consumers.OrderConsumer.as_asgi()),
]
