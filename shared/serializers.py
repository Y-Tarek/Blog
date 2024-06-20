from rest_framework import serializers

class BaseReadDataSerializer(serializers.Serializer):
    """ Read Basic data of some models """
    id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    modified_at = serializers.DateTimeField()

class ReadPostDataSerializer(BaseReadDataSerializer):
    """ Read Basic data of Posts """
    title = serializers.CharField()
    content = serializers.CharField()