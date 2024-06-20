from rest_framework import serializers
from app.models import Category
from shared.serializers import BaseReadDataSerializer, ReadPostDataSerializer

class CategorySerializer(serializers.ModelSerializer):
    """ Category Serializer """
    class Meta:
        """ Category Serializer Meta """
        model = Category
        fields = ("name",)

class BaseReadCategorySerializer(BaseReadDataSerializer):
    """ A Base read serializer for the simple category data """
    name = serializers.CharField()
    slug = serializers.CharField()

class ReadCategorySerializer(BaseReadCategorySerializer):
    """ A Read serializer for the category data with their posts """
    posts = ReadPostDataSerializer(source="post_categories",many=True)