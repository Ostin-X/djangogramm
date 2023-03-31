from django.core.management import BaseCommand
from django.http import request

from posts.views_create_db import create_all_db


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('--------Command executed--------')
        print(create_all_db().content.decode("utf-8"))
