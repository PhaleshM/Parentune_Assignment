from rest_framework import serializers
from .models import UserProfile, Child, Blog, Vlog
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['id','user', 'parent_type']
        extra_kwargs = {'user': {'read_only': True}}

class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = ['id','user', 'name', 'gender', 'date_of_birth']
        extra_kwargs = {'user': {'read_only': True}}

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'published_at', 'updated_at', 'status', 'age_group','gender']

class VlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vlog
        fields = ['id', 'title', 'video_url', 'published_at', 'updated_at', 'status', 'age_group','gender']


class RegisterSerializer(serializers.ModelSerializer):
    parent_type = serializers.ChoiceField(choices=UserProfile.PARENT_TYPE_CHOICES,required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'parent_type']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        UserProfile.objects.create(user=user)
        return user
