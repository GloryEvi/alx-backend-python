from django.db import models


class UnreadMessagesManager(models.Manager):
    """
    Custom manager to filter unread messages for a specific user.
    """
    
    def unread_for_user(self, user):
        """
        Returns unread messages for a specific user where they are the receiver.
        """
        return self.filter(receiver=user, unread=True)
    
    def get_queryset(self):
        """
        Returns the default queryset for unread messages.
        """
        return super().get_queryset().filter(unread=True)