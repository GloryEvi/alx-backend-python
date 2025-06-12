from django.db import models
from django.contrib.auth.models import User

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        return self.filter(read=False).exclude(user=user).only('id', 'content', 'user', 'created_at')

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    
    objects = models.Manager()  # Default manager
    unread = UnreadMessagesManager()  # Custom manager
    
    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"History for message {self.message.id}: {self.old_content[:50]}"