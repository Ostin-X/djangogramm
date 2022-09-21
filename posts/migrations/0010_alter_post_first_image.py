# Generated by Django 4.1.1 on 2022-09-21 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_post_first_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='first_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='+', to='posts.image'),
        ),
    ]