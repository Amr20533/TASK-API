from django.db import models
from django.contrib.auth.models import User

class TaskStatus(models.TextChoices):
    PENDING = 'pending'
    INPROGRESS = 'inprogress'
    FINISHED = 'finished'

class TaskPriority(models.TextChoices):
    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'

class Task(models.Model):
    user = models.ForeignKey(User, related_name= "user_tasks", on_delete= models.CASCADE, default= "", blank= False)
    title = models.CharField(max_length= 250, blank= False, default= "")
    description = models.CharField(max_length= 1300, blank= False, default= "")
    priority = models.CharField(max_length= 60, blank= False, default= TaskPriority.LOW , choices= TaskPriority.choices)
    due_date = models.DateTimeField(max_length= 90, blank= False)
    status = models.CharField(max_length= 60, blank= False, default= TaskStatus.PENDING , choices= TaskStatus.choices)
    image = models.ImageField(upload_to= "task_images", default= "default_task.jpg")
    created_at = models.DateField(auto_now_add= True)

