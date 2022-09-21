# Generated by Django 4.1.1 on 2022-09-21 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_post_object_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='first_image_new',
            new_name='first_image',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='object_id',
            new_name='image_id',
        ),
        migrations.AlterField(
            model_name='image',
            name='is_first',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='first_image_new', to='posts.post'),
        ),
    ]
