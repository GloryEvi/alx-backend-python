from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is the sender or receiver of the message
        if hasattr(obj, 'sender'):
            return obj.sender == request.user or obj.receiver == request.user
        # For conversations, check if user is a participant
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        return False

class IsParticipant(permissions.BasePermission):
    """
    Permission to check if user is participant in conversation
    """
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        # For messages, check if user is sender or receiver
        if hasattr(obj, 'sender'):
            return obj.sender == request.user or obj.receiver == request.user
        return False
    
class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access messages.
    """
    
    def has_permission(self, request, view):
        # Only authenticated users can access the API
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # For Message objects, check if user is participant in the conversation
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
        
        # For Conversation objects, check if user is a participant
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        
        return False

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is the sender or receiver of the message
        if hasattr(obj, 'sender'):
            return obj.sender == request.user or obj.receiver == request.user
        # For conversations, check if user is a participant
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        return False

class IsParticipant(permissions.BasePermission):
    """
    Permission to check if user is participant in conversation
    """
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        # For messages, check if user is sender or receiver
        if hasattr(obj, 'sender'):
            return obj.sender == request.user or obj.receiver == request.user
        return False