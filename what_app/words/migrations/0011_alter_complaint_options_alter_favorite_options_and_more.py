# Generated by Django 4.0.5 on 2022-07-03 14:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('words', '0010_rename_usersmars_usersmarks'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='complaint',
            options={'verbose_name': 'Жалоба', 'verbose_name_plural': 'Жалобы'},
        ),
        migrations.AlterModelOptions(
            name='favorite',
            options={'verbose_name': 'Избранное', 'verbose_name_plural': 'Избранное'},
        ),
        migrations.AlterModelOptions(
            name='profileuser',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterModelOptions(
            name='word',
            options={'ordering': ['-id'], 'verbose_name': 'Слово', 'verbose_name_plural': 'Все слова'},
        ),
        migrations.AlterField(
            model_name='complaint',
            name='complaint_add_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='fav_add_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='profileuser',
            name='reg',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='word',
            name='definition',
            field=models.TextField(verbose_name='Определение'),
        ),
        migrations.AlterField(
            model_name='word',
            name='dislike',
            field=models.IntegerField(default=0, verbose_name='Дизлайки'),
        ),
        migrations.AlterField(
            model_name='word',
            name='example',
            field=models.TextField(verbose_name='Пример'),
        ),
        migrations.AlterField(
            model_name='word',
            name='like',
            field=models.IntegerField(default=0, verbose_name='Лайки'),
        ),
        migrations.AlterField(
            model_name='word',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='word',
            name='word',
            field=models.CharField(max_length=150, unique=True, verbose_name='Слово'),
        ),
        migrations.AlterField(
            model_name='word',
            name='word_add_date',
            field=models.DateField(auto_now=True, verbose_name='Дата добавления'),
        ),
    ]