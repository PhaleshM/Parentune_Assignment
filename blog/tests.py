from django.test import TestCase
from django.contrib.auth.models import User
from .models import *
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from urllib.parse import urlencode

class UserProfileTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        url = reverse('register')
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.user = User.objects.get(username=data['username'])

    def test_userprofile_created(self):
        """
        Test if UserProfile is created when a User is created.
        """
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, UserProfile)
        self.assertEqual(self.user.profile.user, self.user)

    def test_userprofile_str(self):
        """
        Test the string representation of UserProfile.
        """
        self.assertEqual(str(self.user.profile), self.user.username)

    def test_userprofile_parent_type(self):
        """
        Test if parent type is set correctly in UserProfile.
        """
        self.assertEqual(self.user.profile.parent_type, UserProfile.PARENT_TYPE_CHOICES[0][0])

    def test_userprofile_bio(self):
        """
        Test if bio field is blank by default in UserProfile.
        """
        self.assertEqual(self.user.profile.bio, None)

    def test_userprofile_update_bio(self):
        """
        Test updating the bio field in UserProfile.
        """
        new_bio = 'This is a test bio.'
        self.user.profile.bio = new_bio
        self.user.profile.save()
        self.assertEqual(self.user.profile.bio, new_bio)


class UserChildrenTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        url = reverse('register')
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.user = User.objects.get(username=data['username'])

    def test_create_child(self):
        """
        Test creating a new child for a user.
        """
        url = reverse('child-list')
        data = {
            'user': self.user.id,
            'name': 'Test Child',
            'gender': 'male',
            'date_of_birth': '2020-01-01'
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Child.objects.count(), 1)
        child = Child.objects.get(user=self.user)
        self.assertEqual(child.name, 'Test Child')
        self.assertEqual(str(child.date_of_birth), '2020-01-01')
    
    def test_retrieve_child(self):
        """
        Test retrieving a child for a user.
        """
        child = Child.objects.create(user=self.user, name='Test Child',gender= 'male', date_of_birth='2020-01-01')
        url = reverse('child-detail', kwargs={'pk': child.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Child')

    def test_update_child(self):
        """
        Test updating a child for a user.
        """
        child = Child.objects.create(user=self.user, name='Test Child', gender= 'male', date_of_birth='2020-01-01')
        url = reverse('child-detail', kwargs={'pk': child.pk})
        data = {'name': 'New Name',
                'gender': 'female',
            'date_of_birth': '2022-01-01'}
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        child.refresh_from_db()
        self.assertEqual(child.name, 'New Name')

    def test_delete_child(self):
        """
        Test deleting a child for a user.
        """
        child = Child.objects.create(user=self.user, name='Test Child',gender= 'male', date_of_birth='2020-01-01')
        url = reverse('child-detail', kwargs={'pk': child.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Child.objects.count(), 0)


class BlogVlogTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_create_blog(self):
        """
        Test creating a new blog.
        """
        url = reverse('blog-list')
        data = {
            'title': 'Test Blog',
            'content': 'This is a test blog content.',
            'author': self.user.id
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Blog.objects.count(), 1)
        blog = Blog.objects.get(author=self.user)
        self.assertEqual(blog.title, 'Test Blog')
        self.assertEqual(blog.content, 'This is a test blog content.')

    def test_create_vlog(self):
        """
        Test creating a new vlog.
        """
        url = reverse('vlog-list')
        data = {
            'title': 'Test Vlog',
            'video_url': 'https://www.youtube.com/watch?v=LsT3etnkRAY',
            'author': self.user.id
        }
        self.client.force_authenticate(user=self.user)
        response =self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vlog.objects.count(), 1)
        vlog = Vlog.objects.get(author=self.user)
        self.assertEqual(vlog.title, 'Test Vlog')
        self.assertEqual(vlog.video_url, 'https://www.youtube.com/watch?v=LsT3etnkRAY')

    def test_update_vlog(self):
        """
        Test creating a new vlog.
        """
        vlog=Vlog.objects.create(title='Test Vlog',video_url='https://www.youtube.com/watch?v=LsT3etnkRAY',author= self.user)
        url = reverse('vlog-detail',kwargs={'pk': vlog.pk})
        data = {
            'title': 'Updated Vlog',
            'video_url': 'https://www.youtube.com/watch?v=LsT3etnkRAY',
        }
        self.client.force_authenticate(user=self.user)
        response =self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        vlog.refresh_from_db()
        self.assertEqual(vlog.title, 'Updated Vlog')
        self.assertEqual(vlog.video_url, 'https://www.youtube.com/watch?v=LsT3etnkRAY')

    def test_update_blog(self):
        """
        Test creating a new blog.
        """
        blog=Blog.objects.create(title='Test Blog',content='This is a test blog content.',author= self.user)
        url = reverse('blog-detail',kwargs={'pk': blog.pk})
        data = {
            'title': 'Updated Blog',
            'content': 'This is a updated blog content.',
        }
        self.client.force_authenticate(user=self.user)
        response =self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        blog.refresh_from_db()
        self.assertEqual(blog.title, 'Updated Blog')
        self.assertEqual(blog.content, 'This is a updated blog content.')