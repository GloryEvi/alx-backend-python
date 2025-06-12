from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django_chat.models import Message

@cache_page(60)
def message_list(request):
    messages = Message.objects.select_related('user').order_by('-created_at')
    return render(request, 'chats/message_list.html', {'messages': messages})