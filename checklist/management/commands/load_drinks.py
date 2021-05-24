from os import name
from django.core.management.base import BaseCommand
from checklist.models import Drink
import csv
from django_countries import countries

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('load_file', type=str, help='get file with data for a table')

    def handle(self, *args, **options):
        with open(options['load_file'], encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            for row in csv_reader:
                drink_name = row[0]
                country_code = row[3]
                if Drink.objects.filter(name=drink_name).exists():
                    continue
                Drink.objects.create(name=drink_name, country=country_code)