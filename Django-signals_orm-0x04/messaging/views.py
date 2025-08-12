from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from messaging_app.chats import models
from .models import Message, Notification, MessageHistory
from django.views.decorators.cache import cache_page


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    """
    View that allows a user to delete their account.
    This will delete the user and all associated data.
    """
    try:
        user = request.user
        
        Message.objects.filter(sender=user).delete()
        Message.objects.filter(receiver=user).delete()
        
        # Delete associated notifications
        Notification.objects.filter(user=user).delete()
        
        # Logout the user before deletion
        logout(request)
        
        # Delete the user account
        user.delete()
        
        return Response({
            'message': 'User account deleted successfully'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': 'Failed to delete user account',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@login_required
@require_http_methods(["DELETE"])
@csrf_exempt
def delete_user_view(request):
    """
    Alternative function-based view for deleting user account.
    """
    try:
        user = request.user
        
        # Clean up related data
        Message.objects.filter(sender=user).delete()
        Message.objects.filter(receiver=user).delete()
        Notification.objects.filter(user=user).delete()
        
        # Logout and delete user
        logout(request)
        user.delete()
        
        return JsonResponse({
            'message': 'User account deleted successfully'
        }, status=200)
        
    except Exception as e:
        return JsonResponse({
            'error': 'Failed to delete user account',
            'details': str(e)
        }, status=500)
    
@cache_page(60)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def conversation_messages(request, conversation_id):
    """
    View to display a list of messages in a conversation with 60 seconds caching.
    """
    try:
        # Get messages for the conversation
        messages = Message.objects.filter(
            models.Q(sender=request.user, receiver__id=conversation_id) |
            models.Q(sender__id=conversation_id, receiver=request.user)
        ).order_by('timestamp')
        
        
        message_data = []
        for message in messages:
            message_data.append({
                'id': message.id,
                'sender': message.sender.username,
                'receiver': message.receiver.username,
                'content': message.content,
                'timestamp': message.timestamp,
                'unread': message.unread
            })
        
        return Response({
            'messages': message_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': 'Failed to retrieve messages'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)