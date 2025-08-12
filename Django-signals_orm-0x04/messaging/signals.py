from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory


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