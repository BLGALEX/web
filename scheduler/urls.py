from django.urls import path

from .views import RegistrationAPIView

app_name = 'scheduler'
urlpatterns = [
    path('user/', RegistrationAPIView.as_view()),
]