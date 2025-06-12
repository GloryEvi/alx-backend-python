from django.db.models.signals import pre_save
from django.dispatch import receiver
from .Models import Message, MessageHistory


@receiver(pre_save, sender=Message)
def save_message_history(sender, instance, **kwargs):
    """
    Signal to save the old content of a message before it's updated.
    """
    if instance.pk:  # Only for existing messages (updates, not new creations)
        try:
            old_message = Message.objects.get(pk=instance.pk)
            # Check if content has actually changed
            if old_message.content != instance.content:
                # Save the old content to history
                MessageHistory.objects.create(
                    message=old_message,
                    old_content=old_message.content
                )
                # Mark the message as edited
                instance.edited = True
        except Message.DoesNotExist:
            pass  # New message, no history to save