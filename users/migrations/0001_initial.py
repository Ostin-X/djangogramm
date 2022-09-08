# Generated by Django 4.1.1 on 2022-09-08 08:15

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
                ('is_invisible', models.BooleanField(default=False, verbose_name="Сором'змива дупа")),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
