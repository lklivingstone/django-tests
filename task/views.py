from .models import Task, Tag
from .serializers import TaskSerializer, TagSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
import ast

allowed_fields = set(["title", "description", "due_date", "tags", "status"])


class TaskRetrieveUpdateDestroyAPIView(APIView):
    allowed_methods = ["GET", "POST", "PUT", "DELETE"]
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            try:
                tasks = Task.objects.get(id=pk)
                serializer = TaskSerializer(tasks)

            except Task.DoesNotExist:
                return Response(
                    {"error": f"Task with id = {pk} not found."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        else:
            tasks = Task.objects.all()
            serializer = TaskSerializer(tasks, many=True)

        serializer_data = serializer.data
        return Response(serializer_data, status=status.HTTP_200_OK)

    def post(self, request):
        #  dictionary not in
        if not set(request.data.keys()).issubset(allowed_fields):
            return Response(
                {"message": "Request body contains illegal elements"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = TaskSerializer(data=request.data)

        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            error_string = str(e)
            error_dict = ast.literal_eval(error_string)
            error_message = error_dict.get("__all__")[0]
            return Response(
                {"error": error_message},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def put(self, request, pk):
        if not set(request.data.keys()).issubset(allowed_fields):
            return Response(
                {"message": "Request body contains illegal elements"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = TaskSerializer(data=request.data)

        try:
            task = Task.objects.get(id=pk)
            serializer = TaskSerializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        except Task.DoesNotExist:
            return Response(
                {"error": f"Task with id = {pk} not found."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValidationError as e:
            error_string = str(e)
            error_dict = ast.literal_eval(error_string)
            error_message = error_dict.get("__all__")[0]
            return Response(
                {"error": error_message},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        try:
            task = Task.objects.get(id=pk)
            task.delete()
            return Response({"message": f"Task with id = {pk} deleted."}, status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response(
                {"error": f"Task with id = {pk} not found."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class TagListCreateAPIView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagRetrieveUpdateDestroyAPIView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            return None

    def get(self, request, pk):
        tag = self.get_object(pk)
        if tag:
            serializer = TagSerializer(tag)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"error": f"Tag with id = {pk} not found."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def put(self, request, pk):
        tag = self.get_object(pk)
        if tag:
            serializer = TagSerializer(tag, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"error": f"Tag with id = {pk} not found."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk):
        tag = self.get_object(pk)
        if tag:
            tag.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"error": f"Tag with id = {pk} not found."},
            status=status.HTTP_400_BAD_REQUEST,
        )
