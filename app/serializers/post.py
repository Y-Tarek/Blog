from rest_framework import serializers
from app.models import Post, Comment
from shared.serializers import BaseReadDataSerializer
from .category import BaseReadCategorySerializer
from .tag import BaseReadTagSerializer
from users.serializers import ReadProfileSerializer
from users.models import Profile

class PostSerializer(serializers.ModelSerializer):
    """ Post Serializer """

    class Meta:
        model = Post
        fields = ("title","content","categories","tags",)
    
    def create(self, validated_data):
        """ Create Method for posts. """
        user = self.context.get("request").user
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            raise serializers.ValidationError("Profile does not exist for this user.")
        validated_data['author'] = profile
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    """ Comment Serializer """

    class Meta:
        model = Comment
        fields = ("post","content",)


    def create(self, validated_data):
        """ Create Method for posts. """
        user = self.context.get("request").user
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            raise serializers.ValidationError("Profile does not exist for this user.")
        validated_data['author'] = profile
        return super().create(validated_data)



class BaseReadCommentSerializer(BaseReadDataSerializer):
    """ Base Read Comment Serializer """
    
    content = serializers.CharField()
    post_id = serializers.IntegerField(source="post.id")


class ReadCommentSerializer(BaseReadCommentSerializer):
    """ Read Comment Serializer """
    
    author = ReadProfileSerializer()


class BaseReadPostSerializer(BaseReadDataSerializer):
    """ Read Post Serializer """

    title = serializers.CharField()
    content = serializers.CharField()
    categories = BaseReadCategorySerializer(many=True)
    tags = BaseReadTagSerializer(many=True)
    comments = BaseReadCommentSerializer(source="post_comments", many=True)
    author = ReadProfileSerializer()