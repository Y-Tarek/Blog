from rest_framework import status
from django.urls import reverse
from app.models import Post, Comment
from users.models import User, Profile
from app.serializers import ReadCommentSerializer
from app.apis import CommentAPIView
from .base import BaseTest

class CommentAPIViewTestCase(BaseTest):
    """ Comment Test class """

    def setUp(self):
        super().setUp()
        self.comment1 = Comment.objects.create(author=self.userprofile, post=self.base_post, content="comment content")
        self.post1 = Post.objects.create(title='Test Post', content='test-post-content', author = self.userprofile)
        self.post2 = Post.objects.create(title='Post 2', content='Content 2', author = self.userprofile)
        self.other_user = User.objects.create_user(username='testuser2', password='testpass2', email="test2@gmail.com", first_name="test2", last_name="user2")
        self.otheruserprofile = Profile.objects.create(user=self.other_user)

        self.url = reverse('app:comments-list')
        self.detail_url = reverse('app:comments-detail', kwargs={'pk': self.comment1.pk})

    ########### SUCCESS TESTS ########### 

    def test_url(self):
        """
        def is testing the response for url
        """
        self.validate_url(self.url, CommentAPIView)
    
    def test_list_comments(self):
        """ Test retrieving list of comments for authenticated user """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 1) 
    
    def test_create_comment(self):
        """ Test creating a new comment for authenticated user """
        data = {'post': self.post1.pk, 'content': 'Free Content'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_update_comment_authenticated(self):
        """ Test updating a comment by authenticated user """
        data = {'content': 'Updated Comment Content'}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment1.refresh_from_db()
        self.assertEqual(self.comment1.content, 'Updated Comment Content')

    def test_retrieve_comment_authenticated(self):
        """ Test retrieve a comment by authenticated user """
        response = self.client.get(self.detail_url)
        serializer = ReadCommentSerializer(self.comment1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
    
    def test_delete_comment_authenticated(self):
        """ Test deleting a comment by authenticated user """
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(id=self.comment1.id).exists())
    
     ########### FALIURE TESTS ########### 

    def test_patch_with_other_user(self):
        """ Test updating comment with another user """
        self.client.logout()
        self.client.force_authenticate(user=self.other_user)
        data = {'content': 'Updated comment'}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_with_other_user(self):
        """ Test deleteing a comment wiht another user """
        self.client.logout()
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_comment_with_missing_data(self):
        """ Test creating a new comment with missing data"""
        data = {'content': '2nd Content'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('post', response.data)
        self.assertEqual(response.data['post'][0], 'This field is required.')
        
    
    def test_create_comment_invalid_data(self):
        """ Test creating a new comment with invalid data"""
        data = {'post': self.base_post.pk, 'content': ''}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('content', response.data)
        self.assertEqual(response.data['content'][0], 'This field may not be blank.')