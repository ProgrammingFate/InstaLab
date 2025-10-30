from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from apps.core.models import JobListing, JobApplication, JobCategory, Post, Like, Comment

User = get_user_model()


class UserModelTest(TestCase):
    """Tests for CustomUser model"""
    
    def setUp(self):
        self.student = User.objects.create_user(
            username='student1',
            nickname='student_nick',
            email='student@test.com',
            password='testpass123',
            user_type='student',
            course='Engenharia',
            university='UFSC'
        )
        
        self.company = User.objects.create_user(
            username='company1',
            nickname='company_nick',
            email='company@test.com',
            password='testpass123',
            user_type='company',
            company_name='Tech Company'
        )
    
    def test_user_creation(self):
        """Test user creation with all fields"""
        self.assertEqual(self.student.username, 'student1')
        self.assertTrue(self.student.is_student())
        self.assertFalse(self.student.is_company())
        
        self.assertEqual(self.company.username, 'company1')
        self.assertTrue(self.company.is_company())
        self.assertFalse(self.company.is_student())
    
    def test_user_str(self):
        """Test string representation"""
        self.assertEqual(str(self.student), 'student_nick')
        self.assertEqual(str(self.company), 'company_nick')


class JobListingModelTest(TestCase):
    """Tests for JobListing model"""
    
    def setUp(self):
        self.company = User.objects.create_user(
            username='testcompany',
            nickname='test_company',
            email='company@test.com',
            password='testpass123',
            user_type='company'
        )
        
        self.category = JobCategory.objects.create(
            name='Tecnologia',
            slug='tecnologia'
        )
        
        self.job = JobListing.objects.create(
            company=self.company,
            title='Desenvolvedor Python',
            description='Vaga para desenvolvedor Python com conhecimento em Django' * 5,
            requirements='Python, Django, Git',
            job_type='full_time',
            experience_level='junior',
            location='São Paulo',
            category=self.category,
            status='active'
        )
    
    def test_job_creation(self):
        """Test job listing creation"""
        self.assertEqual(self.job.title, 'Desenvolvedor Python')
        self.assertEqual(self.job.company, self.company)
        self.assertEqual(self.job.status, 'active')
        self.assertTrue(self.job.is_active)
    
    def test_job_methods(self):
        """Test job listing methods"""
        self.assertFalse(self.job.is_deadline_passed())
        
        self.job.close()
        self.assertEqual(self.job.status, 'closed')
        
        self.job.activate()
        self.assertEqual(self.job.status, 'active')
    
    def test_applications_count(self):
        """Test applications count property"""
        self.assertEqual(self.job.applications_count, 0)


class JobApplicationModelTest(TestCase):
    """Tests for JobApplication model"""
    
    def setUp(self):
        self.student = User.objects.create_user(
            username='student1',
            nickname='student',
            email='student@test.com',
            password='testpass123',
            user_type='student'
        )
        
        self.company = User.objects.create_user(
            username='company1',
            nickname='company',
            email='company@test.com',
            password='testpass123',
            user_type='company'
        )
        
        self.job = JobListing.objects.create(
            company=self.company,
            title='Test Job',
            description='A test job description' * 10,
            requirements='Test requirements',
            job_type='full_time',
            location='Test City'
        )
        
        self.application = JobApplication.objects.create(
            job=self.job,
            applicant=self.student,
            cover_letter='This is my cover letter explaining why I am a good fit for this position.' * 3
        )
    
    def test_application_creation(self):
        """Test job application creation"""
        self.assertEqual(self.application.job, self.job)
        self.assertEqual(self.application.applicant, self.student)
        self.assertEqual(self.application.status, 'pending')
    
    def test_application_methods(self):
        """Test application status methods"""
        self.application.approve()
        self.assertEqual(self.application.status, 'approved')
        
        self.application.reject()
        self.assertEqual(self.application.status, 'rejected')
        
        self.application.set_interview()
        self.assertEqual(self.application.status, 'interview')


class PostModelTest(TestCase):
    """Tests for Post model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            nickname='test',
            email='test@test.com',
            password='testpass123'
        )
        
        self.post = Post.objects.create(
            author=self.user,
            content='Test post content',
            post_type='text',
            is_active=True
        )
    
    def test_post_creation(self):
        """Test post creation"""
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.content, 'Test post content')
        self.assertTrue(self.post.is_active)
    
    def test_post_likes(self):
        """Test post likes"""
        self.assertEqual(self.post.likes_count, 0)
        
        Like.objects.create(user=self.user, post=self.post)
        self.assertEqual(self.post.likes_count, 1)
    
    def test_post_comments(self):
        """Test post comments"""
        self.assertEqual(self.post.comments_count, 0)
        
        Comment.objects.create(
            user=self.user,
            post=self.post,
            content='Test comment'
        )
        self.assertEqual(self.post.comments_count, 1)
    
    def test_hashtags(self):
        """Test hashtag parsing"""
        self.post.hashtags = 'python, django, web'
        self.post.save()
        
        tags = self.post.get_hashtags_list()
        self.assertEqual(len(tags), 3)
        self.assertIn('python', tags)