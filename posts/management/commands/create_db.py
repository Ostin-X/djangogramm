from django.core.management import BaseCommand
from django.http import request

from posts.views_create_db import create_all_db


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument('first')
    def handle(self, *args, **options):
        print('--------Command executed--------')
        print(create_all_db(request).content.decode("utf-8"))
