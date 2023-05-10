from django.core.management import BaseCommand

from posts.views_create_db import create_all_db


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('--------Command executed--------')
        print(create_all_db())
