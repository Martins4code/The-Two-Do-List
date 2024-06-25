from django.urls import path
from .views import Task_list, Task_detail, Create_task,Update_task,Delete_task,Login,Register
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("register/", Register.as_view(), name= "register"),
    path("login/", Login.as_view(), name= "login"),
    path("logout/", LogoutView.as_view(next_page='login'), name="logout"),
    path("", Task_list.as_view(), name= "tasks"),
    
    
    path("task/<int:pk>/", Task_detail.as_view(), name= "task"),
    path("task_create/", Create_task.as_view(), name= "create"),
    path("task_update/<int:pk>/", Update_task.as_view(), name= "update"),
    path("task_delete/<int:pk>/", Delete_task.as_view(), name= "delete"),
]
 