# Generated by Django 4.0.5 on 2022-07-02 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0003_alter_profileuser_reg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileuser',
            name='reg',
            field=models.DateField(auto_now=True),
        ),
    ]