from django.contrib import admin
from django import forms
from .models import *

admin.site.register(ProfileUser)
admin.site.register(Complaint)
admin.site.register(Word)
admin.site.register(Favorite)
