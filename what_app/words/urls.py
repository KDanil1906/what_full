from django.urls import path
from .views import *


urlpatterns = [
    path('', HomeView.as_view(), name='main'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
]
