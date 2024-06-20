from rest_framework.test import APITestCase, APIClient
from users.models import User, Profile
from app.models import Category, Tag, Post
from django.urls import resolve
from importlib import import_module


class BaseTest(APITestCase):
      """ Base Test class for creating a user and authenticate it. """
      def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass', email="test@gmail.com", first_name="test", last_name="user")
        self.userprofile = Profile.objects.create(user=self.user)
        self.base_category = Category.objects.create(name="Base Category", slug = "base-category")
        self.base_tag = Tag.objects.create(name="Base Category", slug = "base-category")
        self.base_post = Post.objects.create(title='Base Post', content='test-base-content', author = self.userprofile)
        self.client.force_authenticate(user=self.user)  

      def validate_url(self, reverse_url, api_class):
        """this function for router validation"""
        func = resolve(reverse_url).func
        module = import_module(func.__module__)
        view = getattr(module, func.__name__)
        self.assertEquals(view, api_class)

      def validate_sample_url(self, reverse_url, api_class):
        """
        this function for path validation
        """
        view = resolve(reverse_url).func.view_class
        self.assertEquals(view, api_class)