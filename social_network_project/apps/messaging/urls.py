from django.urls import path
from .views import ChatView, MessageListView, send_message
app_name = "messaging"
urlpatterns = [
    path('chat/', ChatView.as_view(), name='chat'),
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('send/', send_message, name='send_message'),
]