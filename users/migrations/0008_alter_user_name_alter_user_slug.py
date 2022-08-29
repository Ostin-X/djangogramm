# Generated by Django 4.1 on 2022-08-29 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_user_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=100, verbose_name="Ім'я"),
        ),
        migrations.AlterField(
            model_name='user',
            name='slug',
            field=models.SlugField(max_length=100, unique=True, verbose_name='URL'),
        ),
    ]