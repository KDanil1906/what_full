# Generated by Django 4.0.5 on 2022-07-02 11:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0006_alter_profileuser_reg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='complaint_add_date',
            field=models.DateField(default=datetime.date(2022, 7, 2)),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='fav_add_date',
            field=models.DateField(default=datetime.date(2022, 7, 2)),
        ),
        migrations.AlterField(
            model_name='profileuser',
            name='reg',
            field=models.DateField(default=datetime.date(2022, 7, 2)),
        ),
        migrations.AlterField(
            model_name='word',
            name='word_add_date',
            field=models.DateField(default=datetime.date(2022, 7, 2)),
        ),
    ]
