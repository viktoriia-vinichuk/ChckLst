from os import name
from django.core.management.base import BaseCommand
from checklist.models import Author
import csv

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('load_file', type=str, help='get file with data for a table')

    def handle(self, *args, **options):
        with open(options['load_file'], encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            for row in csv_reader:
                author_name = row[0]
                if Author.objects.filter(name=author_name).exists():
                    continue
                Author.objects.create(name=author_name)