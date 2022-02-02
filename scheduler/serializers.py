from dataclasses import dataclass
from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import User, Task


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        write_only=True
    )

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        password = data.get('password', None)
        username = data.get('username', None)
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        if username is None:
            raise serializers.ValidationError(
                'An username is required to log in.'
            )
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this username and password was not found.'
            )
        
        return {
            'username': user.username
        }


class TaskSerializer(serializers.ModelSerializer):

    title=serializers.CharField(max_length=255)
    
    class Meta:
        fields = ('title', )
        model = Task

    def validate(self, data):
        title = data.get('title', '')

        try:
            task = Task.objects.get(title=title)
        except:
            return data

        if task.title == title:
            raise serializers.ValidationError('Task with such name already exist')
        else:
            return data
        
class TaskIdSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', )
        model = Task

    def validate(self, data):
        id = data.get('id', '')
        username = data.get('username', '')
        try:
            Task.objects.get(id=id)
        except:
            raise serializers.ValidationError(
                'Not such task'
            )
        task = Task.objects.get(id=id)
        if task.user.username != username:
            raise serializers.ValidationError(
                'Not such task'
            )
        return data