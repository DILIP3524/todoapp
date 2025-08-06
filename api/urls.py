from django.urls import path
from .views import tasks_ApiView, task_detailApiView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
urlpatterns =[
    path('all_tasks' , tasks_ApiView , name="task_list"),
    path('get_task/<int:pk>' , task_detailApiView , name="task_detail"),

     # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]