from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class CreateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('first_name', 'last_name', 'email', 'password')
        extra_keywords = {
            'first_name': {'requied': True, 'allow_blank' : False}, 
            'last_name': {'requied': True, 'allow_blank' : False}, 
            'email' : {'requied': True, 'allow_blank' : False}, 
            'password' : {'requied': True, 'allow_blank' : False, 'min-length' : 8}
        }

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('profile_pic', 'date_of_birth', 'gender', 'phone_number' , 'experience_level', 'address')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User 
        fields = ('id', 'first_name', 'last_name', 'email', 'profile')

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        if profile_data:
            profile_serializer = ProfileSerializer(instance.profile, data=profile_data, partial=True)
            if profile_serializer.is_valid(raise_exception=True):
                profile_serializer.save()

        return super().update(instance, validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)
