from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Count
from django_filters.rest_framework import DjangoFilterBackend

from apps.core.models import Post, JobListing, JobApplication, Comment, Like
from apps.accounts.models import CustomUser
from .serializers import (
    UserSerializer, PostSerializer, JobListingSerializer,
    JobApplicationSerializer, CommentSerializer, LikeSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing user profiles.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'nickname', 'company_name']
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing posts.
    """
    queryset = Post.objects.filter(is_active=True).select_related('author').prefetch_related('likes', 'comments')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content', 'hashtags', 'location']
    ordering_fields = ['created_at', 'likes__count']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by post type
        post_type = self.request.query_params.get('post_type', None)
        if post_type:
            queryset = queryset.filter(post_type=post_type)
        
        # Filter by author
        author_id = self.request.query_params.get('author', None)
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        
        # Feed: posts from followed users
        feed = self.request.query_params.get('feed', None)
        if feed == 'true':
            following_users = self.request.user.following.values_list('following', flat=True)
            queryset = queryset.filter(
                Q(author__in=following_users) | Q(author=self.request.user)
            )
        
        return queryset.annotate(
            likes_count=Count('likes'),
            comments_count=Count('comments')
        )
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Toggle like on a post"""
        post = self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if not created:
            like.delete()
            return Response({'liked': False, 'likes_count': post.likes.count()})
        
        return Response({'liked': True, 'likes_count': post.likes.count()})
    
    @action(detail=True, methods=['post'])
    def comment(self, request, pk=None):
        """Add a comment to a post"""
        post = self.get_object()
        serializer = CommentSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """Get all comments for a post"""
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)


class JobListingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing job listings.
    """
    queryset = JobListing.objects.filter(status='active').select_related('company', 'category')
    serializer_class = JobListingSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'job_type', 'experience_level', 'status']
    search_fields = ['title', 'description', 'tags', 'company__company_name']
    ordering_fields = ['created_at', 'applications__count']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by location
        location = self.request.query_params.get('location', None)
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        # My jobs (for companies)
        my_jobs = self.request.query_params.get('my_jobs', None)
        if my_jobs == 'true':
            queryset = JobListing.objects.filter(company=self.request.user)
        
        return queryset.annotate(applications_count=Count('applications'))
    
    def perform_create(self, serializer):
        if not self.request.user.is_company():
            raise PermissionError("Apenas empresas podem criar vagas.")
        serializer.save(company=self.request.user)
    
    @action(detail=True, methods=['post'])
    def apply(self, request, pk=None):
        """Apply to a job"""
        job = self.get_object()
        
        if not request.user.is_student():
            return Response(
                {'error': 'Apenas estudantes podem se candidatar.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if JobApplication.objects.filter(job=job, applicant=request.user).exists():
            return Response(
                {'error': 'Você já se candidatou para esta vaga.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = JobApplicationSerializer(
            data={**request.data, 'job_id': job.id},
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save(applicant=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def applications(self, request, pk=None):
        """Get all applications for a job (company only)"""
        job = self.get_object()
        
        if job.company != request.user:
            return Response(
                {'error': 'Você não tem permissão para ver estas candidaturas.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        applications = job.applications.all()
        serializer = JobApplicationSerializer(
            applications, many=True, context={'request': request}
        )
        return Response(serializer.data)


class JobApplicationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing job applications.
    """
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        # Students see their own applications
        if self.request.user.is_student():
            return JobApplication.objects.filter(applicant=self.request.user)
        
        # Companies see applications to their jobs
        return JobApplication.objects.filter(job__company=self.request.user)
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Update application status (company only)"""
        application = self.get_object()
        
        if application.job.company != request.user:
            return Response(
                {'error': 'Você não tem permissão para atualizar esta candidatura.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        new_status = request.data.get('status')
        if new_status not in dict(JobApplication.STATUS_CHOICES):
            return Response(
                {'error': 'Status inválido.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        application.status = new_status
        application.company_notes = request.data.get('company_notes', application.company_notes)
        application.save()
        
        serializer = self.get_serializer(application)
        return Response(serializer.data)
