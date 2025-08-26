from django.test import TestCase
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.message = Message.objects.create(sender=self.user, content='Hello, World!')

    def test_message_creation(self):
        self.assertEqual(self.message.sender, self.user)
        self.assertEqual(self.message.content, 'Hello, World!')

    def test_message_str(self):
        self.assertEqual(str(self.message), f'{self.user.username}: {self.message.content}')