from django.urls import path
from .views import * 

urlpatterns = [
    path('tasks/', getTasks ,name= "get-all-tasks"),
    path('tasks/addTask', addNewTask ,name= "add-task"),


]
