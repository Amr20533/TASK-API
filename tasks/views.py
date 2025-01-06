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


@api_view(['GET'])
def getTaskById(request, task_id):
    try:
        task = get_object_or_404(Task, id=task_id)

        task_serializer = TaskSerializer(task, many = False)

        return Response({"tasks" : task_serializer.data}, status= status.HTTP_200_OK)
    
    except Task.DoesNotExist as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

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


@api_view(['PUT'])
def editTask(request, task_id):
    data = request.data
    try:
        task = get_object_or_404(Task, id=task_id)

        due_date = data.get('due_date')
        if due_date:
            if isinstance(due_date, str):
                naive_due_date = timezone.datetime.fromisoformat(due_date)
            else:
                naive_due_date = due_date
            aware_due_date = timezone.make_aware(naive_due_date)
        else:
            aware_due_date = task.due_date 

        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.priority = data.get('priority', task.priority)
        task.due_date = aware_due_date
        task.status = data.get('status', task.status)
        task.image = data.get('image', task.image)

        task.save()

        serializer = TaskSerializer(task)

        return Response({"task": serializer.data}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteTask(request, task_id):
    try:
        task = get_object_or_404(Task, id=task_id)

        task.delete()

        return Response({"detail" : "Task is Successfully Deleted!!"}, status= status.HTTP_200_OK)
    
    except Task.DoesNotExist as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)