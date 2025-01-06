from django.urls import path
from .views import * 

urlpatterns = [
    path('tasks/', getTasks ,name= "get-all-tasks"),
    path('tasks/task/<int:task_id>', getTaskById ,name= "get-task"),
    path('tasks/addTask', addNewTask ,name= "add-task"),
    path('tasks/editTask/<int:task_id>', editTask ,name= "edit-task"),
    path('tasks/deletTask/<int:task_id>', deleteTask ,name= "delete-task"),


]
