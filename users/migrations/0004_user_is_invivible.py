# Generated by Django 4.1 on 2022-08-29 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_invivible',
            field=models.BooleanField(default=False, verbose_name="Сором'змива дупа"),
        ),
    ]
