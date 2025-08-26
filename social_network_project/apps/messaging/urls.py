from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    # Chat URLs
    path('', views.conversations_list, name='conversations_list'),
    path('chat/', views.chat_view, name='chat'),
    path('chat/<int:conversation_id>/', views.chat_view, name='chat_view'),
    path('search/', views.search_users, name='search_users'),
    
    # Stories URLs
    path('stories/', views.stories_feed, name='stories_feed'),
    path('stories/create/', views.CreateStoryView.as_view(), name='create_story'),
    path('stories/<int:story_id>/', views.view_story, name='view_story'),
    path('stories/<int:story_id>/delete/', views.delete_story, name='delete_story'),
]