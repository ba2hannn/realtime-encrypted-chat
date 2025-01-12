# routing.py
from django.urls import path,re_path
from .consumers import ChatConsumer, PrivateChatConsumer, VoiceChatConsumer

websocket_urlpatterns = [
    path('ws/notification/<str:room_name>/', ChatConsumer.as_asgi()),
    path('ws/private_notification/<str:chat_name>/', PrivateChatConsumer.as_asgi()),
    re_path(r'ws/voice_chat/(?P<room_name>\w+)/$', VoiceChatConsumer.as_asgi()),
]