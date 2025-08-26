from django.contrib import admin
from .models import ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "recipient", "timestamp")
    search_fields = ("sender__username", "sender__nickname", "recipient__username", "recipient__nickname", "content")
    list_filter = ("timestamp",)
    ordering = ("-timestamp",)