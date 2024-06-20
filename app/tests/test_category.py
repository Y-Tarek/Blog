from rest_framework import status
from django.urls import reverse
from app.models import Category
from app.serializers import ReadCategorySerializer
from app.apis import CategoryAPIView
from .base import BaseTest

class CategoryAPIViewTestCase(BaseTest):
    """ Category Test class """

    def setUp(self):
        super().setUp()
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.url = reverse('app:categories-list')
        self.detail_url = reverse('app:categories-detail', kwargs={'pk': self.category.pk})
    
    def test_url(self):
        """
        def is testing the response for url
        """
        self.validate_url(self.url, CategoryAPIView)
    
    ########### SUCCESS TESTS ########### 

    def test_category_list(self):
        """ Test category success list """
        response = self.client.get(self.url)
        categories = Category.objects.all()
        serializer = ReadCategorySerializer(categories, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), serializer.data)
    
    def test_get_single_category(self):
        """ Test category success retrieve """
        response = self.client.get(self.detail_url)
        category = Category.objects.get(pk=self.category.pk)
        serializer = ReadCategorySerializer(category)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
    
    def test_create_category(self):
        """ Test category success creation """
        data = {'name': 'New Category'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 3)
    
    def test_update_category(self):
        """ Test category success update """
        data = {'name': 'Updated Category'}
        response = self.client.patch(self.detail_url, data)
        self.category.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.category.slug, 'updated-category')
    
    def test_delete_category(self):
        """ Test category success delete """
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 1)
    
    def test_search_category(self):
        response = self.client.get(self.url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Test Category')

    
     ########### FALIURE TESTS ########### 

    def test_get_category_list_unauthorized(self):
        """ Test category list unauthorized """
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
    
    
    def test_create_category_missing_fields(self):
        """ Test creating a category with missing fields """
        data = {'slug': 'new-category'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
