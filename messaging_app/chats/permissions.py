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