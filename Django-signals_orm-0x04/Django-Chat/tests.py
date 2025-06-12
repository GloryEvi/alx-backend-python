from django.test import TestCase
from django.contrib.auth.models import User
from .Models import Message, MessageHistory


class MessageHistoryTestCase(TestCase):
    def setUp(self):
        """Set up test users for testing"""
        self.sender = User.objects.create_user(
            username='sender',
            email='sender@example.com',
            password='testpass123'
        )
        self.receiver = User.objects.create_user(
            username='receiver',
            email='receiver@example.com',
            password='testpass123'
        )

    def test_message_creation_no_history(self):
        """Test that creating a new message doesn't create history"""
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Original message content"
        )
        
        self.assertEqual(message.edited, False)
        self.assertEqual(MessageHistory.objects.count(), 0)

    def test_message_edit_creates_history(self):
        """Test that editing a message creates history and marks it as edited"""
        # Create initial message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Original content"
        )
        
        # Verify no history initially
        self.assertEqual(MessageHistory.objects.count(), 0)
        self.assertEqual(message.edited, False)
        
        # Edit the message
        message.content = "Edited content"
        message.save()
        
        # Verify history was created
        self.assertEqual(MessageHistory.objects.count(), 1)
        
        # Refresh message from database
        message.refresh_from_db()
        self.assertEqual(message.edited, True)
        
        # Verify history content
        history = MessageHistory.objects.first()
        self.assertEqual(history.message, message)
        self.assertEqual(history.old_content, "Original content")
        self.assertIsNotNone(history.edited_at)

    def test_multiple_edits_create_multiple_history_records(self):
        """Test that multiple edits create multiple history records"""
        # Create initial message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Original content"
        )
        
        # First edit
        message.content = "First edit"
        message.save()
        
        # Second edit
        message.content = "Second edit"
        message.save()
        
        # Should have 2 history records
        self.assertEqual(MessageHistory.objects.count(), 2)
        
        # Verify history contents
        histories = MessageHistory.objects.order_by('edited_at')
        self.assertEqual(histories[0].old_content, "Original content")
        self.assertEqual(histories[1].old_content, "First edit")

    def test_saving_without_content_change_no_history(self):
        """Test that saving without changing content doesn't create history"""
        # Create initial message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Original content"
        )
        
        # Save without changing content
        message.save()
        
        # Should not create history
        self.assertEqual(MessageHistory.objects.count(), 0)
        message.refresh_from_db()
        self.assertEqual(message.edited, False)