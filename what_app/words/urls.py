from django.urls import path
from .views import *


urlpatterns = [
    path('', HomeView.as_view(), name='main'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('complain/<int:id>/', ComplainView.as_view(), name='complain'),
    path('add_word/', add_word, name='add_word'),
    path('ordering/<str:kind>', OrderingView.as_view(), name='ordering'),
    path('search/<str:type>/<str:value>', Search.as_view(), name='search'),
    path('favorite/<int:id>', favorite, name='favorite'),
    path('marks/<int:id>/<int:mark>', marks, name='marks'),
]
