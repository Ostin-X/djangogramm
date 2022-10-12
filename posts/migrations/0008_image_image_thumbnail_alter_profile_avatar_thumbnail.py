# Generated by Django 4.1.2 on 2022-10-12 12:58

from django.db import migrations, models
import posts.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_profile_avatar_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='image_thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Тамбнейл'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar_thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to=posts.models.path_and_rename_thumbnail, verbose_name='Тамбнейл'),
        ),
    ]
