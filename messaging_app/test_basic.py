import pytest
from django.test import TestCase
from django.contrib.auth.models import User

class BasicTests(TestCase):
    def test_user_creation(self):
        """Test user can be created"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        
    def test_basic_math(self):
        """Basic test to ensure pytest is working"""
        assert 1 + 1 == 2
        assert 2 * 3 == 6