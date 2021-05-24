from os import name
from django.core.management.base import BaseCommand
from checklist.models import Movie
import csv

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('load_file', type=str, help='get file with data for a table')

    def handle(self, *args, **options):
        with open(options['load_file'], encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            for row in csv_reader:
                movie_title = row[0]
                movie_year = row[1]
                if Movie.objects.filter(title=movie_title).exists():
                    continue
                Movie.objects.create(title=movie_title, year=movie_year)