from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Read permissions are allowed to any request,
    but write permissions are only allowed to the owner of the object.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            # Check if the user is the sender or receiver of the message
            if hasattr(obj, 'sender'):
                return obj.sender == request.user or obj.receiver == request.user
            # For conversations, check if user is a participant
            if hasattr(obj, 'participants'):
                return request.user in obj.participants.all()
            return False
        
        # Write permissions (POST, PUT, PATCH, DELETE) are only allowed to the owner
        if request.method in ["PUT", "PATCH", "DELETE"]:
            # Check if the user is the sender or receiver of the message
            if hasattr(obj, 'sender'):
                return obj.sender == request.user
            # For conversations, check if user is a participant
            if hasattr(obj, 'participants'):
                return request.user in obj.participants.all()
        
        return False


class IsParticipant(permissions.BasePermission):
    """
    Permission to check if user is participant in conversation.
    Allows read access to participants, write access based on method type.
    """
    
    def has_object_permission(self, request, view, obj):
        # Check if user is participant first
        is_participant = False
        
        if hasattr(obj, 'participants'):
            is_participant = request.user in obj.participants.all()
        elif hasattr(obj, 'sender'):
            is_participant = (obj.sender == request.user or 
                            obj.receiver == request.user)
        
        if not is_participant:
            return False
            
        # For safe methods, allow if participant
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # For write methods (PUT, PATCH, DELETE), additional checks
        if request.method in ["PUT", "PATCH", "DELETE"]:
            if hasattr(obj, 'sender'):
                # Only sender can edit/delete their own messages
                return obj.sender == request.user
            # For conversations, all participants can modify
            return True
            
        return False


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access messages.
    Handles different HTTP methods (GET, POST, PUT, PATCH, DELETE) appropriately.
    """
    
    def has_permission(self, request, view):
        # Only authenticated users can access the API
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Check if user is participant
        is_participant = False
        
        # For Message objects, check if user is participant in the conversation
        if hasattr(obj, 'conversation'):
            is_participant = request.user in obj.conversation.participants.all()
        # For Conversation objects, check if user is a participant
        elif hasattr(obj, 'participants'):
            is_participant = request.user in obj.participants.all()
        
        if not is_participant:
            return False
            
        # Allow safe methods (GET, HEAD, OPTIONS) for participants
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # For modification methods (PUT, PATCH, DELETE)
        if request.method in ["PUT", "PATCH", "DELETE"]:
            # For messages, only the sender can edit/delete
            if hasattr(obj, 'conversation') and hasattr(obj, 'sender'):
                return obj.sender == request.user
            # For conversations, all participants can modify
            return True
            
        return False