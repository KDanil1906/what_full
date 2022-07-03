import datetime

from django.db import models
from django.contrib.auth.models import User


class ProfileUser(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    reg = models.DateField(default=datetime.date.today())

    def __str__(self):
        return self.name.username


class Complaint(models.Model):
    user_id = models.ForeignKey(ProfileUser, on_delete=models.CASCADE)
    word_id = models.ForeignKey('Word', on_delete=models.CASCADE)
    explanation = models.TextField()
    complaint_add_date = models.DateField(default=datetime.date.today())


class Word(models.Model):
    user_id = models.ForeignKey(ProfileUser, on_delete=models.CASCADE)
    word = models.CharField(max_length=150, unique=True)
    definition = models.TextField()
    example = models.TextField()
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    word_add_date = models.DateField(default=datetime.date.today())

    def __str__(self):
        return self.word


class Favorite(models.Model):
    user_id = models.ForeignKey(ProfileUser, on_delete=models.CASCADE)
    word_id = models.ForeignKey(Word, on_delete=models.CASCADE)
    fav_add_date = models.DateField(default=datetime.date.today())

    def __str__(self):
        return self.word_id.word


class UsersMarks(models.Model):
    user_id = models.ForeignKey(ProfileUser, on_delete=models.CASCADE)
    word_id = models.ForeignKey(Word, on_delete=models.CASCADE)
    mark = models.BooleanField()
