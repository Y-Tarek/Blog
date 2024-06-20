from rest_framework import serializers
from users.models import User, Profile
from shared.utility import Base64FileField

class ProfileSerializer(serializers.ModelSerializer):
    """ Profile Serializer. """

    profile_picture = Base64FileField(required=False)
    class Meta:
        """ The Meta class for ProfileSerializer """
        model = Profile
        fields = ('profile_picture', 'bio',)

class RegisterSerializer(serializers.ModelSerializer):
    """ User Serializer for Registering user to the system. """

    profile_data = ProfileSerializer(required=False)

    class Meta:
        """ The Meta class for UserSerializer """
        model = User
        fields = ("email","username","password","profile_data",)
    
    def create(self, validated_data):
        """ The Create Method for registering new user. """

        profile_data = validated_data.pop('profile_data', None)
        user = User.objects.create_user(**validated_data)

        if profile_data:
            Profile.objects.create(user=user, **profile_data)
        return user

class LoginSerializer(serializers.Serializer):
    """ Login Serilaier for authorizing user data. """
    email = serializers.EmailField()
    password = serializers.CharField()
