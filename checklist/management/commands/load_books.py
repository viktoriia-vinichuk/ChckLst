from os import name
from django.core.management.base import BaseCommand, CommandError
from checklist.models import Book, Author
import csv

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('load_file', type=str, help='get file with data for a table')

    def handle(self, *args, **options):
        with open(options['load_file'], encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            for row in csv_reader:
                author_name = row[0]
                book_title = row[1]
                try:
                    author_obj = Author.objects.get(name=author_name)
                except Author.DoesNotExist:
                    raise CommandError(f'Author "{author_name}" does not exists.')
                if Book.objects.filter(title=book_title).exists():
                    continue
                new_book = Book.objects.create(title=book_title)
                new_book.author.add(author_obj)