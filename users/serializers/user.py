from rest_framework import serializers

class ReadProfileSerializer(serializers.Serializer):
    """ Read Only Serilaizer For Profile data """

    user_id = serializers.IntegerField(source="user.id")
    username = serializers.CharField(source="user.username")
    email = serializers.CharField(source="user.email")
    profile_picture = serializers.FileField()
    bio = serializers.CharField()