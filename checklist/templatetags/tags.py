from django import template

register = template.Library()

@register.simple_tag
def is_read(book, user):
    a = user in [item.user for item in book.choice_set.all()]
    return a

@register.simple_tag
def is_all_read(books, user):
    num_books = books.count()
    try:
        user_num_books = user.choice.books.all().count()
        if num_books == user_num_books:
            return True
    except:
        return False
