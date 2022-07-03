from django.db import models
from django.contrib.auth.models import User


class ProfileUser(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    reg = models.DateField(auto_now=True)

    def __str__(self):
        return self.name.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Complaint(models.Model):
    user_id = models.ForeignKey(ProfileUser, on_delete=models.CASCADE)
    word_id = models.ForeignKey('Word', on_delete=models.CASCADE)
    explanation = models.TextField()
    complaint_add_date = models.DateField(auto_now=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Жалоба'
        verbose_name_plural = 'Жалобы'


class Word(models.Model):
    user_id = models.ForeignKey(ProfileUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    word = models.CharField(max_length=150, unique=True, verbose_name='Слово')
    definition = models.TextField(verbose_name='Определение')
    example = models.TextField(verbose_name='Пример')
    like = models.IntegerField(default=0, verbose_name='Лайки')
    dislike = models.IntegerField(default=0, verbose_name='Дизлайки')
    word_add_date = models.DateField(auto_now=True, verbose_name='Дата добавления')

    def __str__(self):
        return self.word

    class Meta:
        ordering = ['-id']
        verbose_name = 'Слово'
        verbose_name_plural = 'Все слова'


class Favorite(models.Model):
    user_id = models.ForeignKey(ProfileUser, on_delete=models.CASCADE)
    word_id = models.ForeignKey(Word, on_delete=models.CASCADE)
    fav_add_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.word_id.word

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class UsersMarks(models.Model):
    user_id = models.ForeignKey(ProfileUser, on_delete=models.CASCADE)
    word_id = models.ForeignKey(Word, on_delete=models.CASCADE)
    mark = models.BooleanField()

