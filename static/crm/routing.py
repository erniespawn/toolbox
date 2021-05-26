from django.urls import re_path

from . import chatbox, sendSMS



websocket_urlpatterns = [
    re_path(r'ws/sendSMS/(?P<room_name>\w+)/$', sendSMS.ChatRoomConsumer.as_asgi()),
    re_path(r'ws/chatbox/(?P<room_name>\w+)/$', chatbox.ChatRoomConsumer.as_asgi()),
    ]
