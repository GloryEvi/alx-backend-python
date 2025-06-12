from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, MessageHistory

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    # Only log if this is an update (not a new message)
    if instance.pk:
        try:
            # Get the old version of the message
            old_message = Message.objects.get(pk=instance.pk)
            # Check if content has changed
            if old_message.content != instance.content:
                # Save the old content to history
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_message.content
                )
                # Mark the message as edited
                instance.edited = True
        except Message.DoesNotExist:
            pass

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    # Only log if this is an update (not a new message)
    if instance.pk:
        try:
            # Get the old version of the message
            old_message = Message.objects.get(pk=instance.pk)
            # Check if content has changed
            if old_message.content != instance.content:
                # Save the old content to history
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_message.content
                )
                # Mark the message as edited
                instance.edited = True
        except Message.DoesNotExist:
            pass

@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    # Delete all messages associated with the user
    Message.objects.filter(user=instance).delete()
    
    # MessageHistory will be automatically deleted due to CASCADE relationship