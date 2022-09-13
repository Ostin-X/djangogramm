# Generated by Django 4.1.1 on 2022-09-13 09:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, null=True, verbose_name='Про себе')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=users.models.path_and_rename, verbose_name='Аватарка')),
                ('avatar_thumbnail', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Тамбнейл')),
                ('is_invisible', models.BooleanField(default=False, verbose_name="Сором'язлива дупа")),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профіль',
                'verbose_name_plural': 'Профілі',
                'ordering': ['user'],
            },
        ),
    ]
