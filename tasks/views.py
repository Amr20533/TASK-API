from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getTasks(request):
    user = request.user
    if not request.user.is_authenticated:
        raise PermissionDenied("You must be logged in to access this resource.")
    
    task = Task.objects.filter(user = user)

    task_serializer = TaskSerializer(task, many = True)

    return Response({
        "status" : "success",
        "tasks" : task_serializer.data
        }, status= status.HTTP_200_OK)

# To Get Data for admin and staff users [''this method not used'']
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def getAllTasks(request):
    if not request.user.is_authenticated:
        raise PermissionDenied("You must be logged in to access this resource.")
    
    if not request.user.is_staff:
        raise PermissionDenied("You do not have permission to access this resource.")

    task = Task.objects.all()

    task_serializer = TaskSerializer(task, many = True)

    return Response({
        "status" : "success",
        "tasks" : task_serializer.data
        }, status= status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getTaskById(request, task_id):
    user = request.user
    try:
        if not request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to access this resource.")

        task = get_object_or_404(Task, id=task_id, user = user)

        task_serializer = TaskSerializer(task, many = False)
    
        return Response({
            "status" : "success",
            "task" : task_serializer.data
            }, status= status.HTTP_200_OK)

    except Task.DoesNotExist as e:
        return Response({
            "status" : "failed",
            "error": str(e)
            }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({
            "status" : "failed",
            "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def addNewTask(request):
    data = request.data
    try:
        if not request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to access this resource.")

        due_date = data.get('due_date')
        if due_date:
            if isinstance(due_date, str):
                naive_due_date = timezone.datetime.fromisoformat(due_date)
            else:
                naive_due_date = due_date
            aware_due_date = timezone.make_aware(naive_due_date)
        else:
            aware_due_date = None

        task = Task.objects.create(
            user=request.user,
            title=data['title'],
            description=data['description'],
            priority=data.get('priority', TaskPriority.LOW),
            due_date=aware_due_date,
            status=data.get('status', TaskStatus.PENDING),
            image= data.get("image", 'task_images/default_task.png'),
        )

        task_serializer = TaskSerializer(task)
        return Response({
            "status": "success",
            "task": task_serializer.data
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            "status": "failed",
            "error": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def editTask(request, task_id):
    user = request.user
    data = request.data
    try:
        if not request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to access this resource.")
    
        task = get_object_or_404(Task, id=task_id, user = user)

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

        task_serializer = TaskSerializer(task)

        return Response({
                "status" : "success",
                "task" : task_serializer.data
                }, status= status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            "status" : "failed",
            "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteTask(request, task_id):
    user = request.user
    try:
        if not request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to access this resource.")

        task = get_object_or_404(Task, id=task_id, user = user)

        task.delete()

        return Response({
                "status" : "success",
                "task" : {}
            }, status= status.HTTP_204_NO_CONTENT)
    
    except Task.DoesNotExist as e:
        return Response({
            "status" : "failed",
            "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({
            "status" : "failed",
            "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
