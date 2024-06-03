from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# UserProfile model to extend the built-in User model with additional parent information
class UserProfile(models.Model):
    PARENT_TYPE_CHOICES = [
        ('first-time', 'First-time Parent'),
        ('experienced', 'Experienced Parent'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    parent_type = models.CharField(max_length=20, choices=PARENT_TYPE_CHOICES, default='first-time')

    def __str__(self):
        return self.user.username

# Child model to store information about the children

class Child(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='children')
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.user.username})"

# Blog model to store blog content
AGE_GROUP_CHOICES = [
    ('all', 'All'),
    ('0-1', '0-1'),
    ('1-3', '1-3'),
    ('3-7', '3-7'),
    ('7-10', '7-10'),
    ]

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('any', 'Any'),
    ]
class Blog(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    age_group = models.CharField(max_length=5, choices=AGE_GROUP_CHOICES, default='all')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='any')

    class Meta:
        ordering = ('-published_at',)

    def __str__(self):
        return self.title

# Vlog model to store vlog content
class Vlog(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vlog_posts')
    video_url = models.URLField(max_length=200)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    age_group = models.CharField(max_length=5, choices=AGE_GROUP_CHOICES, default='all')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES,default='any')
    class Meta:
        ordering = ('-published_at',)

    def __str__(self):
        return self.title
