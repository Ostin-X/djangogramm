# Generated by Django 4.1.1 on 2022-09-12 08:49

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_profile_is_invisible_alter_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avatar_thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to=users.models.path_and_rename, verbose_name='Тамбнейл'),
        ),
    ]
