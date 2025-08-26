from django.test import TestCase
from django.urls import reverse
from .models import User

class UserModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            nickname='testnickname'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.nickname, 'testnickname')

class UserViewsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            nickname='testnickname'
        )

    def test_login_view(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # Redirect on successful login

    def test_register_view(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'password1': 'newpassword',
            'password2': 'newpassword',
            'nickname': 'newnickname'
        })
        self.assertEqual(response.status_code, 302)  # Redirect on successful registration

    def test_profile_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)  # Profile page should be accessible
        self.assertContains(response, 'testnickname')  # Check if nickname is displayed