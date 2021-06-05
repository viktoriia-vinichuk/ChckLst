from django import template

from .. import views

register = template.Library()


@register.simple_tag
def is_marked(object, user):
    return user in [item.user for item in object.choice_set.all()]


@register.simple_tag
def is_all_read(user):
    return views.is_all_read(user)


@register.simple_tag
def is_all_watched(user):
    return views.is_all_watched(user)


@register.simple_tag
def is_all_eaten(user):
    return views.is_all_eaten(user)


@register.simple_tag
def is_all_drunk(user):
    return views.is_all_drunk(user)
