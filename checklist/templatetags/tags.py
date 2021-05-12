from django import template

register = template.Library()

@register.simple_tag
def is_read(book, user):
    a = user in [item.user for item in book.choice_set.all()]
    return a