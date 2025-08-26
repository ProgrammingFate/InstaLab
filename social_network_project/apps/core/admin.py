from django.contrib import admin
from .models import Post, JobCategory, JobListing, JobApplication

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'created_at')
    search_fields = ('content',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(JobListing)
class JobListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'category', 'status', 'priority', 'spots_available', 'created_at')
    list_filter = ('status', 'priority', 'category', 'remote_work', 'created_at')
    search_fields = ('title', 'company__company_name', 'company__nickname', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'job', 'status', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('applicant__nickname', 'job__title')
    ordering = ('-applied_at',)