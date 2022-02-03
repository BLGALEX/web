import mimetypes

from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http.response import HttpResponse

from .serializers import *
from .models import *


class RegistrationAPIView(APIView):

    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TodosAPIView(APIView):
    permission_classes = (AllowAny,)
    task_serializer = TaskSerializer
    user_serializer = LoginSerializer

    def post(self, request):
        data = request.data
        if not isinstance(request.data, dict):
            data = request.data.dict()
        task = data
        user = data
        user_serializer = self.user_serializer(data=user)
        user_serializer.is_valid(raise_exception=True)

        task_serializer = self.task_serializer(data=task)
        task_serializer.is_valid(raise_exception=True)

        task["user"] = User.objects.get(username=user["username"])
        instance = Task.objects.create(
            user=task["user"], title=task["title"], complete=task.get("complete", False)
        )

        response = task_serializer.data
        response["id"] = instance.id

        return Response(response, status=status.HTTP_201_CREATED)

    def get(self, request):
        data = request.data
        if not isinstance(request.data, dict):
            data = request.data.dict()
        print(data)
        user = data
        user_serializer = self.user_serializer(data=user)
        user_serializer.is_valid(raise_exception=True)
        user_id = User.objects.get(username=user["username"])

        tasks = list(
            Task.objects.filter(user=user_id).values("id", "title", "complete")
        )
        response = {"tasks": tasks}

        return Response(response, status=status.HTTP_200_OK)


class TodoAPIView(APIView):
    permission_classes = (AllowAny,)
    task_id_serializer = TaskIdSerializer
    user_serializer = LoginSerializer
    task_serializer = TaskSerializer

    def get(self, request, task_id):
        data = request.data
        if not isinstance(request.data, dict):
            data = request.data.dict()
        user = data
        user_serializer = self.user_serializer(data=user)
        user_serializer.is_valid(raise_exception=True)

        data = {"id": task_id, "username": user["username"]}
        task_id_serializer = self.task_id_serializer(data=data)
        task_id_serializer.is_valid(raise_exception=True)

        task = Task.objects.filter(id=task_id).values("id", "title", "complete")[0]
        response = {"task": task}
        return Response(response, status=status.HTTP_200_OK)

    def put(self, request, task_id):
        data = request.data
        if not isinstance(request.data, dict):
            data = request.data.dict()
        user = data
        task_data = data

        user_serializer = self.user_serializer(data=user)
        user_serializer.is_valid(raise_exception=True)

        data = {"id": task_id, "username": user["username"]}
        task_id_serializer = self.task_id_serializer(data=data)
        task_id_serializer.is_valid(raise_exception=True)

        task = Task.objects.get(id=task_id)
        title = task_data.get("title", None)
        if title is not None:
            task.title = title
        complete = task_data.get("complete", None)
        if complete is not None:
            task.complete = complete
        task.save()
        task = Task.objects.filter(id=task_id).values("id", "title", "complete")[0]

        return Response({"task": task}, status=status.HTTP_200_OK)

    def delete(self, request, task_id):
        data = request.data
        if not isinstance(request.data, dict):
            data = request.data.dict()
        user = data

        user_serializer = self.user_serializer(data=user)
        user_serializer.is_valid(raise_exception=True)

        data = {"id": task_id, "username": user["username"]}
        task_id_serializer = self.task_id_serializer(data=data)
        task_id_serializer.is_valid(raise_exception=True)

        task = Task.objects.get(id=task_id)
        task.delete()

        return Response({"task": {"title": task.title}}, status=status.HTTP_200_OK)


class FileAPIView(APIView):
    permission_classes = (AllowAny,)
    parser_classes = (FormParser, JSONParser, MultiPartParser)
    file_serializer = FileSerializer
    user_serializer = LoginSerializer

    def post(self, request):
        data = request.data
        if not isinstance(request.data, dict):
            data = request.data.dict()
        user = data
        file_data = data

        user_serializer = self.user_serializer(data=user)
        user_serializer.is_valid(raise_exception=True)
        user = User.objects.get(username=user["username"])
        file_data["user"] = user.id
        file_serializer = self.file_serializer(data=file_data)
        file_serializer.is_valid(raise_exception=True)

        instance = file_serializer.save()
        response = {
            "id": instance.id,
            "file": instance.file.name,
            "size": f"{round((instance.file.size / 1024) / 1024, 2)} Mb",
        }
        return Response(response, status=status.HTTP_201_CREATED)

    def get(self, request, file_name=None):
        data = request.data
        if not isinstance(request.data, dict):
            data = request.data.dict()
        user = data
        user_serializer = self.user_serializer(data=user)
        user_serializer.is_valid(raise_exception=True)
        user_id = User.objects.get(username=user["username"])

        if file_name is None:
            files = File.objects.filter(user=user_id)
            response = []
            for file in files:
                response.append(
                    {
                        "file": file.file.name,
                        "size": f"{round((file.file.size / 1024) / 1024, 2)} Mb",
                        "id": file.id,
                    }
                )
        else:
            files = File.objects.filter(user=user_id, file=file_name)
            if len(files) == 0:
                raise serializers.ValidationError("Not such file")
            file = files[0]
            filepath = file.file.path
            with open(filepath, "rb") as path:
                mime_type, _ = mimetypes.guess_type(filepath)
                response = HttpResponse(path, content_type=mime_type)
            response["Content-Disposition"] = f"attachment; filename={file.file.name}"
            return response

        return Response(response, status=status.HTTP_200_OK)

    def delete(self, request, file_name=None):
        data = request.data
        if not isinstance(request.data, dict):
            data = request.data.dict()
        user = data
        user_serializer = self.user_serializer(data=user)
        user_serializer.is_valid(raise_exception=True)
        user_id = User.objects.get(username=user["username"])

        try:
            file = File.objects.filter(file=file_name, user=user_id)[0]
        except:
            raise serializers.ValidationError("Not such file")
        name = file.file.name
        file.delete()
        file.file.delete(save=False)

        response = {"file": name}
        return Response(response, status=status.HTTP_200_OK)
