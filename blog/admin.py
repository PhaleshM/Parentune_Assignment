from django.contrib import admin
from .models import UserProfile, Child, Blog, Vlog

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'parent_type')
    search_fields = ('user__username', 'parent_type')

@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'gender', 'date_of_birth')
    list_filter = ('gender',)
    search_fields = ('name', 'user__username')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'author', 'published_at', 'status', 'age_group')
    list_filter = ('status', 'author', 'age_group')
    search_fields = ('title', 'content')
    raw_id_fields = ('author',)
    date_hierarchy = 'published_at'
    ordering = ('status', 'published_at')

@admin.register(Vlog)
class VlogAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'author', 'published_at', 'status', 'age_group')
    list_filter = ('status', 'author', 'age_group')
    search_fields = ('title', 'video_url')
    raw_id_fields = ('author',)
    date_hierarchy = 'published_at'
    ordering = ('status', 'published_at')
