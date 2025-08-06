from django.urls import path
from .views import home , delete_task , update_task
urlpatterns =[
    path("" ,home , name='home' ),
    path("delete/<int:task_id>" ,delete_task , name='delete_task' ),
    path("update/<int:task_id>/<str:status>" ,update_task , name='update_task' ),
]