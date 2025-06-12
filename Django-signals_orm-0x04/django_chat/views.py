from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from .models import Message, MessageHistory

@login_required
def message_history(request, message_id):
    message = get_object_or_404(Message, id=message_id, user=request.user)
    history = MessageHistory.objects.filter(message=message).order_by('-edited_at')
    
    context = {
        'message': message,
        'history': history,
    }
    return render(request, 'django_chat/message_history.html', context)

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Your account has been successfully deleted.')
        return redirect('admin:index')
    
    return render(request, 'django_chat/delete_user.html')

def threaded_messages(request):
    root_messages = Message.objects.filter(parent_message__isnull=True).select_related('user').prefetch_related(
        'replies__user',
        'replies__replies__user',
        'replies__replies__replies__user'
    ).order_by('-created_at')
    
    context = {
        'messages': root_messages,
    }
    return render(request, 'django_chat/threaded_messages.html', context)

@login_required
def unread_inbox(request):
    # Use custom manager with optimized query
    unread_messages = Message.unread.unread_for_user(request.user).select_related('user').order_by('-created_at')
    
    context = {
        'unread_messages': unread_messages,
    }
    return render(request, 'django_chat/unread_inbox.html', context)