from django.urls import path
from .views import *


urlpatterns = [
    path('', HomeView.as_view(), name='main'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('complain/<int:id>', СomplainView.as_view(), name='complain'),
    path('add_word/', add_word, name='add_word'),
    path('search/', Search.as_view(), name='search'),
]
