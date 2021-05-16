from django import template
import random

register = template.Library()

@register.simple_tag
def is_read(book, user):
    a = user in [item.user for item in book.choice_set.all()]
    return a

@register.simple_tag
def random_book(book_list, user):
    rand_books = []
    for book in book_list:
        if user not in [item.user for item in book.choice_set.all()]:
            rand_books.append(book)
    if len(rand_books) > 0:
        return random.choice(rand_books)
    else:
        return 'Nice Done! You have marked everything!'
    