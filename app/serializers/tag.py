from rest_framework import serializers
from app.models import Tag
from shared.serializers import BaseReadDataSerializer, ReadPostDataSerializer

class TagSerializer(serializers.ModelSerializer):
    """ Tag Serializer """
    class Meta:
        """ Tag Serializer Meta """
        model = Tag
        fields = ("name",)


class BaseReadTagSerializer(BaseReadDataSerializer):
    name = serializers.CharField()
    slug = serializers.CharField()

class ReadTagSerializer(BaseReadTagSerializer):
    posts = ReadPostDataSerializer(source="post_tags",many=True)