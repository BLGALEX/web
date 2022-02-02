from urllib import response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core import serializers as ser

from .serializers import *
from .models import *

class RegistrationAPIView(APIView):

    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TodosAPIView(APIView):
    permission_classes = (AllowAny,)
    task_serializer = TaskSerializer
    user_serializer = LoginSerializer

    def post(self, request):
        task = request.data.get('task', {})
        user = request.data.get('user', {})

        user_serializer = self.user_serializer(data=user)
        user_serializer.is_valid(raise_exception=True)

        task_serializer = self.task_serializer(data=task)
        task_serializer.is_valid(raise_exception=True)
        
        task['user'] = User.objects.get(username=user['username'])
        instance = Task.objects.create(**task)

        response = task_serializer.data
        response['id'] = instance.id

        return Response(response, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.data.get('user', {})
        user_serializer = self.user_serializer(data=user)
        user_serializer.is_valid(raise_exception=True)
        user_id = User.objects.get(username=user['username'])

        tasks = list(Task.objects.filter(user=user_id).values('id', 'title', 'complete'))
        response = {"tasks": tasks}

        return Response(response, status=status.HTTP_200_OK)


class TodoAPIView(APIView):
    permission_classes = (AllowAny,)
    task_serializer = TaskIdSerializer
    user_serializer = LoginSerializer

    def get(self, request, task_id):
        user = request.data.get('user', {})
        user_serializer = self.user_serializer(data=user)
        user_serializer.is_valid(raise_exception=True)

        task_serializer = self.task_serializer(data={'id': task_id, 'username': user['username']})
        task_serializer.is_valid(raise_exception=True)

        task = Task.objects.filter(id=task_id).values('id', 'title', 'complete')
        response = {"task": task}
        return Response(response, status=status.HTTP_200_OK)

    def put(self, request, task_id):
        user = request.data.get('user', {})
        user_serializer = self.user_serializer(data=user)
        user_serializer.is_valid(raise_exception=True)

        return Response({}, status=status.HTTP_200_OK)