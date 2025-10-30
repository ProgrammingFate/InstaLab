from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.core.models import Post, JobListing, JobApplication, Comment, Like
from apps.accounts.models import CustomUser

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'nickname', 'email', 'user_type',
            'bio', 'avatar', 'company_name', 'company_description',
            'company_website', 'company_instagram', 'course', 
            'university', 'semester'
        ]
        read_only_fields = ['id', 'username']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile (minimal info)"""
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'nickname', 'avatar', 'user_type', 'bio']
        read_only_fields = ['id', 'username', 'nickname', 'user_type']


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model"""
    user = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'content', 'created_at', 'parent']
        read_only_fields = ['id', 'user', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post model"""
    author = UserProfileSerializer(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    user_liked = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id', 'author', 'content', 'image', 'video', 'post_type',
            'created_at', 'updated_at', 'is_active', 'location', 
            'hashtags', 'likes_count', 'comments_count', 'user_liked', 
            'comments'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
    
    def get_user_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(user=request.user, post=obj).exists()
        return False


class JobListingSerializer(serializers.ModelSerializer):
    """Serializer for JobListing model"""
    company = UserProfileSerializer(read_only=True)
    applications_count = serializers.IntegerField(read_only=True)
    is_applied = serializers.SerializerMethodField()
    
    class Meta:
        model = JobListing
        fields = [
            'id', 'company', 'title', 'category', 'description', 
            'requirements', 'benefits', 'job_type', 'experience_level',
            'location', 'salary_range', 'status', 'created_at', 
            'updated_at', 'tags', 'applications_count', 'is_applied'
        ]
        read_only_fields = ['id', 'company', 'created_at', 'updated_at']
    
    def get_is_applied(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return JobApplication.objects.filter(job=obj, applicant=request.user).exists()
        return False


class JobApplicationSerializer(serializers.ModelSerializer):
    """Serializer for JobApplication model"""
    applicant = UserProfileSerializer(read_only=True)
    job = JobListingSerializer(read_only=True)
    job_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = JobApplication
        fields = [
            'id', 'job', 'job_id', 'applicant', 'cover_letter', 
            'resume', 'status', 'applied_at', 'updated_at', 
            'company_notes'
        ]
        read_only_fields = ['id', 'applicant', 'applied_at', 'updated_at', 'job']
    
    def validate_job_id(self, value):
        try:
            job = JobListing.objects.get(id=value, status='active')
            return value
        except JobListing.DoesNotExist:
            raise serializers.ValidationError("Vaga não encontrada ou não está ativa.")
    
    def create(self, validated_data):
        job_id = validated_data.pop('job_id')
        job = JobListing.objects.get(id=job_id)
        validated_data['job'] = job
        return super().create(validated_data)


class LikeSerializer(serializers.ModelSerializer):
    """Serializer for Like model"""
    user = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
