from django.contrib import admin
from .Models import Message, MessageHistory


class MessageHistoryInline(admin.TabularInline):
    model = MessageHistory
    extra = 0
    readonly_fields = ('old_content', 'edited_at')
    can_delete = False


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'timestamp', 'edited')
    list_filter = ('timestamp', 'edited')
    search_fields = ('sender__username', 'receiver__username', 'content')
    readonly_fields = ('timestamp', 'edited')
    inlines = [MessageHistoryInline]


@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ('message', 'old_content', 'edited_at')
    list_filter = ('edited_at',)
    search_fields = ('message__content', 'old_content')
    readonly_fields = ('message', 'old_content', 'edited_at')