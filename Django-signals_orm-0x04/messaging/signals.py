from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth.models import User


@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """
    Signal to automatically create a notification when a new message is created.
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

    # Create message history entry
        MessageHistory.objects.create(
            message=instance,
            content=instance.content,
            action='created'
        )
@receiver(post_save, sender=Message)
def create_message_history(sender, instance, created, **kwargs):
    """
    Signal to create message history when a message is edited.
    """
    if not created and instance.edited:
        MessageHistory.objects.create(
            message=instance,
            content=instance.content,
            action='edited'
        )

@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    """
    Signal to delete all messages, notifications, and message histories 
    associated with a user when the user is deleted.
    """
    # Delete messages where user is sender or receiver
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    
    # Delete notifications for the user
    Notification.objects.filter(user=instance).delete()
    
    # Delete message histories related to user's messages
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()