from django.urls import path

from .views import *

app_name = 'scheduler'
urlpatterns = [
    path('user/register/', RegistrationAPIView.as_view()),
    path('user/login/', LoginAPIView.as_view()),
    path('todo', TodosAPIView.as_view()),
    path('todo/<int:task_id>', TodoAPIView.as_view()),
    path('files/<int:file_id>', FileAPIView.as_view()),
    path('files', FileAPIView.as_view())
]