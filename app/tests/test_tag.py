from rest_framework import status
from django.urls import reverse
from app.models import Tag
from app.serializers import ReadTagSerializer
from app.apis import TagAPIView
from .base import BaseTest

class TagAPIViewTestCase(BaseTest):
    """ tag Test class """

    def setUp(self):
        super().setUp()
        self.tag = Tag.objects.create(name='Test Tag', slug='test-tag')
        self.url = reverse('app:tags-list')
        self.detail_url = reverse('app:tags-detail', kwargs={'pk': self.tag.pk})
    
    def test_url(self):
        """
        def is testing the response for url
        """
        self.validate_url(self.url, TagAPIView)
    
    ########### SUCCESS TESTS ########### 

    def test_tag_list(self):
        """ Test tag success list """
        response = self.client.get(self.url)
        tags = Tag.objects.all()
        serializer = ReadTagSerializer(tags, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), serializer.data)
    
    def test_get_single_tag(self):
        """ Test tag success retrieve """
        response = self.client.get(self.detail_url)
        tag = Tag.objects.get(pk=self.tag.pk)
        serializer = ReadTagSerializer(tag)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
    
    def test_create_tag(self):
        """ Test tag success creation """
        data = {'name': 'New tag'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tag.objects.count(), 3)
    
    def test_update_tag(self):
        """ Test tag success update """
        data = {'name': 'Updated tag'}
        response = self.client.patch(self.detail_url, data)
        self.tag.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.tag.slug, 'updated-tag')
    
    def test_delete_tag(self):
        """ Test tag success delete """
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tag.objects.count(), 1)
    

    
     ########### FALIURE TESTS ########### 

    def test_get_tag_list_unauthorized(self):
        """ Test tag list unauthorized """
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
    
    
    def test_create_tag_missing_fields(self):
        """ Test creating a tag with missing fields """
        data = {'slug': 'new-tag'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
