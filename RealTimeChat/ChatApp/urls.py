from . import views
from django.urls import path

urlpatterns = [
    path('', views.Login, name='login'),
    path('signup/', views.Signup, name='signup'),
    path('logout/', views.Logout, name='logout'),
    path('create_room/', views.RoomCreate, name='create-room'),
    path('forgot-password/', views.ForgotPassword, name='forgot-password'),
    path('voice_chat/<str:voice_chat>/',views.VoiceRoom,name='voice-chat'),
    path('chat_list/',views.ChatList,name='chat-list'),
    path('room_list/',views.RoomList,name='room-list'),
    path('verify_password/', views.verify_room_password, name='verify_room_password'),
]