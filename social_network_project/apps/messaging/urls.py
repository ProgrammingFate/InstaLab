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
    
    # Área Social dos Estudantes
    path('social/', views.student_social_feed, name='student_social_feed'),
    path('social/post/create/', views.create_student_post, name='create_student_post'),
    path('social/post/<int:post_id>/', views.student_post_detail, name='student_post_detail'),
    path('social/post/<int:post_id>/like/', views.toggle_post_like, name='toggle_post_like'),
    
    # Grupos de Estudo
    path('social/groups/', views.study_groups_list, name='study_groups_list'),
    path('social/groups/create/', views.create_study_group, name='create_study_group'),
    path('social/groups/<int:group_id>/join/', views.join_study_group, name='join_study_group'),
    path('social/groups/<int:group_id>/leave/', views.leave_study_group, name='leave_study_group'),
    
    # Conexões entre Estudantes
    path('social/connections/', views.student_connections, name='student_connections'),
    path('social/students/', views.search_students, name='search_students'),
    path('social/connect/<int:user_id>/', views.send_connection_request, name='send_connection_request'),
]