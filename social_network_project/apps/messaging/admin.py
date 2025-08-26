from django.contrib import admin
from .models import Conversation, ChatMessage, Story, StoryView

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'get_participants']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['participants__nickname', 'participants__email']
    filter_horizontal = ['participants']
    
    def get_participants(self, obj):
        return " & ".join([user.nickname for user in obj.participants.all()])
    get_participants.short_description = 'Participantes'

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'conversation', 'timestamp', 'is_read', 'message_type']
    list_filter = ['timestamp', 'is_read', 'message_type']
    search_fields = ['sender__nickname', 'content']
    readonly_fields = ['timestamp']

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'story_type', 'created_at', 'expires_at', 'is_active', 'get_views_count']
    list_filter = ['story_type', 'created_at', 'is_active']
    search_fields = ['title', 'content', 'user__nickname']
    readonly_fields = ['created_at', 'expires_at']
    
    def get_views_count(self, obj):
        return obj.views.count()
    get_views_count.short_description = 'Visualizações'

@admin.register(StoryView)
class StoryViewAdmin(admin.ModelAdmin):
    list_display = ['story', 'viewer', 'viewed_at']
    list_filter = ['viewed_at']
    search_fields = ['story__title', 'viewer__nickname']
    readonly_fields = ['viewed_at']