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
        else:
            return False
    except:
        return False

@register.simple_tag
def is_watched(movie, user):
    a = user in [item.user for item in movie.choice_set.all()]
    return a

@register.simple_tag
def is_all_watched(movies, user):
    num_movies = movies.count()
    try:
        user_num_movies = user.choice.movies.all().count()
        if num_movies == user_num_movies:
            return True
        else:
            return False
    except:
        return False

@register.simple_tag
def is_eaten(food, user):
    a = user in [item.user for item in food.choice_set.all()]
    return a

@register.simple_tag
def is_all_eaten(dishes, user):
    num_dishes = dishes.count()
    try:
        user_num_dishes = user.choice.food.all().count()
        if num_dishes == user_num_dishes:
            return True
        else:
            return False
    except:
        return False

@register.simple_tag
def is_drunk(drink, user):
    a = user in [item.user for item in drink.choice_set.all()]
    return a

@register.simple_tag
def is_all_drunk(drinks, user):
    num_drinks = drinks.count()
    try:
        user_num_drinks = user.choice.drinks.all().count()
        if num_drinks == user_num_drinks:
            return True
        else:
            return False
    except:
        return False