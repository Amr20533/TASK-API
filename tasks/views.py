from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone


@api_view(['GET'])
def getTasks(request):
    task = Task.objects.all()

    task_serializer = TaskSerializer(task, many = True)

    return Response({"tasks" : task_serializer.data}, status= status.HTTP_200_OK)



@api_view(['POST'])
def addNewTask(request):
    data = request.data
    try:
        due_date = data['due_date']

        if isinstance(due_date, str):
            naive_due_date = timezone.datetime.fromisoformat(due_date)
        else:
            naive_due_date = due_date

        aware_due_date = timezone.make_aware(naive_due_date)

        task = Task.objects.create(
            title=data.get('title', ''),
            description=data.get('description', ''),
            priority=data.get('priority', TaskPriority.LOW),
            due_date=aware_due_date,
            status=data.get('status', TaskStatus.PENDING),
            image=data.get('image', "default_task.jpg")
        )

        serializer = TaskSerializer(task)

        return Response({"task": serializer.data}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
