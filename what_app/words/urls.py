from django.urls import path
from .views import *


urlpatterns = [
    path('', HomeView.as_view(), name='main'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('complain/', СomplainView.as_view(), name='complain'),
    path('add_word/', AddWord.as_view(), name='add_word'),
]
