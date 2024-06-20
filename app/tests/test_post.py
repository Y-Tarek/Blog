from rest_framework import status
from django.urls import reverse
from app.models import Post
from users.models import User, Profile
from app.serializers import BaseReadPostSerializer
from app.apis import PostAPIView
from .base import BaseTest

class PostAPIViewTestCase(BaseTest):
    """ post Test class """

    def setUp(self):
        super().setUp()
        self.post1 = Post.objects.create(title='Test Post', content='test-post-content', author = self.userprofile)
        self.post2 = Post.objects.create(title='Post 2', content='Content 2', author = self.userprofile)
        self.other_user = User.objects.create_user(username='testuser2', password='testpass2', email="test2@gmail.com", first_name="test2", last_name="user2")
        self.otheruserprofile = Profile.objects.create(user=self.other_user)

        self.url = reverse('app:posts-list')
        self.detail_url = reverse('app:posts-detail', kwargs={'pk': self.post1.pk})
    
    ########### SUCCESS TESTS ########### 

    def test_url(self):
        """
        def is testing the response for url
        """
        self.validate_url(self.url, PostAPIView)
    
    def test_list_posts(self):
        """ Test retrieving list of posts for authenticated user """
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 3) 
    
    def test_create_post(self):
        """ Test creating a new post for authenticated user """
        data = {'title': 'New Post', 'content': 'New Content', 'categories':[self.base_category.pk], 'tags':[self.base_tag.pk]}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    

    def test_update_post_authenticated(self):
        """ Test updating a post by authenticated user """
        data = {'title': 'Updated Post', 'content': 'Updated Content'}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.title, 'Updated Post')
    
    def test_retrieve_post_authenticated(self):
        """ Test retrieve a post by authenticated user """
        response = self.client.get(self.detail_url)
        serializer = BaseReadPostSerializer(self.post1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
    
    def test_delete_post_authenticated(self):
        """ Test deleting a post by authenticated user """
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.post1.id).exists())

    
    
    ########### FALIURE TESTS ########### 

    def test_patch_with_other_user(self):
        """ Test updating apost with another user """
        self.client.logout()
        self.client.force_authenticate(user=self.other_user)
        data = {'title': 'Updated post'}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_with_other_user(self):
        """ Test deleteing a post wiht another user """
        self.client.logout()
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    
    def test_create_post_with_missing_data(self):
        """ Test creating a new post with missing data"""
        data = {'title': '2nd Post', 'content': '2nd Content'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('categories', response.data)
        self.assertEqual(response.data['categories'][0], 'This field is required.')
        
        self.assertIn('tags', response.data)
        self.assertEqual(response.data['tags'][0], 'This field is required.')
    

    def test_create_post_invalid_data(self):
        """ Test creating a new post with invalid data"""
        data = {'title': 'New Post', 'content': '', 'categories':[self.base_category.pk], 'tags':[self.base_tag.pk]}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('content', response.data)
        self.assertEqual(response.data['content'][0], 'This field may not be blank.')
    
    