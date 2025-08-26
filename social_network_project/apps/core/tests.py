from django.test import TestCase
from .models import Post, UserInteraction

class PostModelTest(TestCase):
    def setUp(self):
        self.post = Post.objects.create(
            title="Test Post",
            content="This is a test post.",
            author="Test Author"
        )

    def test_post_creation(self):
        self.assertEqual(self.post.title, "Test Post")
        self.assertEqual(self.post.content, "This is a test post.")
        self.assertEqual(self.post.author, "Test Author")

class UserInteractionModelTest(TestCase):
    def setUp(self):
        self.interaction = UserInteraction.objects.create(
            user="Test User",
            post=self.post,
            interaction_type="like"
        )

    def test_user_interaction_creation(self):
        self.assertEqual(self.interaction.user, "Test User")
        self.assertEqual(self.interaction.post, self.post)
        self.assertEqual(self.interaction.interaction_type, "like")