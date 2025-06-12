from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification


class MessageNotificationTestCase(TestCase):
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

    def test_message_creation(self):
        """Test that a message can be created successfully"""
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello, this is a test message!"
        )
        
        self.assertEqual(message.sender, self.sender)
        self.assertEqual(message.receiver, self.receiver)
        self.assertEqual(message.content, "Hello, this is a test message!")
        self.assertIsNotNone(message.timestamp)

    def test_automatic_notification_creation(self):
        """Test that a notification is automatically created when a message is sent"""
        # Ensure no notifications exist initially
        self.assertEqual(Notification.objects.count(), 0)
        
        # Create a new message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="This should trigger a notification!"
        )
        
        # Check that a notification was automatically created
        self.assertEqual(Notification.objects.count(), 1)
        
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.message, message)
        self.assertIsNotNone(notification.created_at)

    def test_multiple_messages_create_multiple_notifications(self):
        """Test that multiple messages create multiple notifications"""
        self.assertEqual(Notification.objects.count(), 0)
        
        # Create first message
        Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="First message"
        )
        
        # Create second message
        Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Second message"
        )
        
        # Should have 2 notifications
        self.assertEqual(Notification.objects.count(), 2)
        self.assertEqual(Notification.objects.filter(user=self.receiver).count(), 2)