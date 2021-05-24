from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.models import User
from django.db.models import Count
from .models import Book, Ingredient, Movie, Food, Drink, B_Genre, M_Genre, F_Kind, D_kind, Ingredient
from collections import Counter, OrderedDict
import country_converter
import random

class BookListView(generic.ListView):
    model = Book
    template_name = 'Books_checklist.html'

class MovieListView(generic.ListView):
    model = Movie
    template_name = 'Movies_checklist.html'

class FoodListView(generic.ListView):
    model = Food
    template_name = 'Food_checklist.html'


class DrinkListView(generic.ListView):
    model = Drink
    template_name = 'Drinks_checklist.html'

# GENERAL -------------------------------------------------------------------------------------

def count_all_obj(model):
    return model.objects.all().count()

def centuryFromYear(year):
    roman = OrderedDict()
    
    roman[1000] = 'M'
    roman[900] = 'CM'
    roman[500] = 'D'
    roman[400] = 'CD'
    roman[100] = 'C'
    roman[90] = 'XC'
    roman[50] = 'L'
    roman[40] = 'XL'
    roman[10] = 'X'
    roman[9] = 'IX'
    roman[5] = 'V'
    roman[4] = 'IV'
    roman[1] = 'I'

    def year_to_roman(year):
        for r in roman.keys():
            x, y = divmod(year, r)
            yield roman[r] * x
            year -= (r * x)
            if year <= 0:
                break

    return "".join([a for a in year_to_roman((year + 99) // 100)])

def del_none(*args):
    for arg in args:
        if None in arg:
            del arg[None]

def percentage(part, whole):
    return round(100 * part / whole)

# Checklists ----------------------------------------------------------------------------------

def checklists(request):
    return render(request, 'checklists.html')

# Statictic -----------------------------------------------------------------------------------

def favorite_items(user, model):
    if model == Book:
        books_id = user.choice.books.values_list('id', flat=True).order_by('id')
        books = model.objects.filter(id__in=books_id)
        genres = books.values_list('genre', flat=True).order_by('genre')
        fav_genres = Counter(genres)
        del_none(fav_genres)
        nothing_to_show = 'mark read books to get stats'
        if fav_genres:
            return ', '.join(B_Genre.objects.get(id=k).genre for k in list(fav_genres.keys())[:3])
        else:
            return nothing_to_show
    elif model == Movie:
        movies_id = user.choice.movies.values_list('id', flat=True).order_by('id')
        movies = model.objects.filter(id__in=movies_id)
        genres = movies.values_list('genre', flat=True).order_by('genre')
        years = movies.values_list('year', flat=True).order_by('year')
        fav_genres = Counter(genres)
        fav_years = Counter(years)
        del_none(fav_genres, fav_years)
        nothing_to_show = 'mark watched movies to get stats'
        if fav_genres:
            return (
                ', '.join(M_Genre.objects.get(id=k).genre for k in list(fav_genres.keys())[:3]), 
                centuryFromYear(int(list(fav_years.keys())[0]))
                )
        else:
            return (nothing_to_show, nothing_to_show)
    elif model == Food:
        food_id = user.choice.food.values_list('id', flat=True).order_by('id')
        food = model.objects.filter(id__in=food_id)
        kinds = food.values_list('food_kinds', flat=True).order_by('food_kinds')
        ingredients = food.values_list('food_ingredients', flat=True).order_by('food_ingredients')
        countries = food.values_list('country', flat=True).order_by('country')
        fav_kinds = Counter(kinds)
        fav_ingredients = Counter(ingredients)
        fav_country = Counter(countries)
        del_none(fav_kinds, fav_country, fav_ingredients)
        nothing_to_show = 'mark eaten dishes to get stats'
        need_more_choices = 'mark more eaten dishes to get these stats'
        if fav_country:
            if len(fav_kinds) > 2 and len(fav_ingredients) > 2:
                return (
                    ', '.join(F_Kind.objects.get(id=k).food_kind for k in list(fav_kinds.keys())[:3]), 
                    ', '.join(Ingredient.objects.get(id=k).ingredient for k in list(fav_ingredients.keys())[:3]),
                    country_converter.convert(list(fav_country.keys())[0], src = 'ISO2', to = 'name_short')
                    )
            else:
                return (
                    need_more_choices, 
                    need_more_choices,
                    country_converter.convert(list(fav_country.keys())[0], src = 'ISO2', to = 'name_short')
                    )
        else:
            return (nothing_to_show, nothing_to_show, nothing_to_show)
    elif model == Drink:
        drink_id = user.choice.drinks.values_list('id', flat=True).order_by('id')
        drinks = Drink.objects.filter(id__in=drink_id)
        kinds = drinks.values_list('drink_kinds', flat=True).order_by('drink_kinds')
        ingredients = drinks.values_list('drink_ingredients', flat=True).order_by('drink_ingredients')
        countries = drinks.values_list('country', flat=True).order_by('country')
        fav_kinds = Counter(kinds)
        fav_ingredients = Counter(ingredients)
        fav_country = Counter(countries)
        del_none(fav_kinds, fav_country, fav_ingredients)
        nothing_to_show = 'mark drinks you have tried to get stats'
        need_more_choices = 'mark more tried drinks to get these stats'
        if fav_country:
            if len(fav_kinds) > 2 and len(fav_ingredients) > 2:
                return (
                    ', '.join(D_kind.objects.get(id=k).drink_kind for k in list(fav_kinds.keys())[:3]), 
                    ', '.join(Ingredient.objects.get(id=k).ingredient for k in list(fav_ingredients.keys())[:3]), 
                    country_converter.convert(list(fav_country.keys())[0], src = 'ISO2', to = 'name_short')
                    )
            else:
                return (
                    need_more_choices, 
                    need_more_choices, 
                    country_converter.convert(list(fav_country.keys())[0], src = 'ISO2', to = 'name_short')
                    )
        else:
            return (nothing_to_show, nothing_to_show, nothing_to_show)
    else:
        return 'the given category does not exist'

def stats(request):

    all_books = count_all_obj(Book)
    all_movies = count_all_obj(Movie)
    all_food = count_all_obj(Food)
    all_drinks = count_all_obj(Drink)

    users = User.objects.annotate(
        num_books=Count('choice__books'),
        num_movies=Count('choice__movies'),
        num_food=Count('choice__food'),
        num_drinks=Count('choice__drinks')
    )

    users_count = users.count()

    user = request.user

    user_num_books = user.choice.books.all().count()
    user_num_movies = user.choice.movies.all().count()
    user_num_food = user.choice.food.all().count()
    user_num_drinks = user.choice.drinks.all().count()

    stats_count = (user_num_books, user_num_movies, user_num_food, user_num_drinks)
    stats_exist = True
    if not any(stats_count):
        stats_exist = False 

    less_read = 0
    less_watched = 0
    less_ate = 0
    less_drank = 0
    
    for i in users:
        read = i.num_books
        watched = i.num_movies
        ate = i.num_food
        drank = i.num_drinks
        if read < user_num_books:
            less_read += 1
        if watched < user_num_movies:
            less_watched += 1
        if ate < user_num_food:
            less_ate += 1
        if drank < user_num_drinks:
            less_drank += 1
    
    context = {
        'user_num_books': user_num_books,
        'user_num_movies': user_num_movies,
        'user_num_food': user_num_food,
        'user_num_drinks': user_num_drinks,
        'all_books': all_books,
        'all_movies': all_movies,
        'all_food': all_food,
        'all_drinks': all_drinks,
        'books_percent': percentage(less_read, users_count),
        'movies_percent': percentage(less_watched, users_count),
        'food_percent': percentage(less_ate, users_count),
        'drinks_percent': percentage(less_drank, users_count),
        'user_books_percent': percentage(user_num_books, all_books),
        'user_movies_percent': percentage(user_num_movies, all_movies),
        'user_food_percent': percentage(user_num_food, all_food),
        'user_drinks_percent': percentage(user_num_drinks, all_drinks),
        'fav_book_genres': favorite_items(user, Book),
        'fav_movie_genres': favorite_items(user, Movie)[0],
        'fav_movie_century': favorite_items(user, Movie)[1],
        'fav_food_kinds': favorite_items(user, Food)[0],
        'fav_food_ingredient': favorite_items(user, Food)[1],
        'fav_food_country': favorite_items(user, Food)[2],
        'fav_drink_kinds': favorite_items(user, Drink)[0],
        'fav_drink_ingredient': favorite_items(user, Drink)[1],
        'fav_drink_country': favorite_items(user, Drink)[2],
        'stats_exist': stats_exist,
    }

    return render(request, 'statistic.html', context=context)

# BOOKS ---------------------------------------------------------------------------------------

def is_all_read(l_user):
    num_books = count_all_obj(Book)
    user_num_books = l_user.choice.books.all().count()
    return num_books == user_num_books

def book_checkbox(request):
    if request.is_ajax and request.method == "POST":
        user = request.user
        book = Book.objects.get(id=request.POST['book_id'])
        if request.POST['is_read'] == 'true':
            user.choice.books.add(book)
            response = {'is-all-read': is_all_read(user)}
        else:
            user.choice.books.remove(book)
            response = {'is-all-read': is_all_read(user)}
        return JsonResponse(response)
    else:
        raise Http404

def random_book(request):
    if request.is_ajax() and request.method == "GET":
        response = {'random-book-info': get_random_book(request)}
        return JsonResponse(response)
    else:
        raise Http404

def get_random_book(request):
    user = request.user
    books_id = user.choice.books.values_list('id', flat=True).order_by('id')
    rand_books = Book.objects.exclude(id__in=books_id)
    if rand_books.count() > 0:
        r_book = random.choice(rand_books)
        return str(f'{r_book.title} by {", ".join(str(author) for author in r_book.author.all())}')
    else:
        return 'Nice Done! You have marked everything!'

# MOVIES --------------------------------------------------------------------------------------

def is_all_watched(l_user):
    num_movies = count_all_obj(Movie)
    user_num_movies = l_user.choice.movies.all().count()
    return num_movies == user_num_movies

def movie_checkbox(request):
    if request.is_ajax and request.method == "POST":
        user = request.user
        movie = Movie.objects.get(id=request.POST['movie_id'])
        if request.POST['is_watched'] == 'true':
            user.choice.movies.add(movie)
            response = {'is-all-watched': is_all_watched(user)}
        else:
            user.choice.movies.remove(movie)
            response = {'is-all-watched': is_all_watched(user)}
        return JsonResponse(response)
    else:
        raise Http404

def random_movie(request):
    if request.is_ajax() and request.method == "GET":
        response = {'random-movie-info': get_random_movie(request)}
        return JsonResponse(response)
    else:
        raise Http404

def get_random_movie(request):
    user = request.user
    movies_id = user.choice.movies.values_list('id', flat=True).order_by('id')
    rand_movies = Movie.objects.exclude(id__in=movies_id)
    if rand_movies.count() > 0:
        r_movie = random.choice(rand_movies)
        return str(f'{r_movie.title} ({r_movie.year})')
    else:
        return 'Nice Done! You have marked everything!'

# FOOD ----------------------------------------------------------------------------------------

def is_all_eaten(l_user):
    num_dishes = count_all_obj(Food)
    user_num_dishes = l_user.choice.food.all().count()
    return num_dishes == user_num_dishes


def food_checkbox(request):
    if request.is_ajax and request.method == "POST":
        user = request.user
        dish = Food.objects.get(id=request.POST['dish_id'])
        if request.POST['is_eaten'] == 'true':
            user.choice.food.add(dish)
            response = {'is-all-eaten': is_all_eaten(user)}
        else:
            user.choice.food.remove(dish)
            response = {'is-all-eaten': is_all_eaten(user)}
        return JsonResponse(response)
    else:
        raise Http404

def random_dish(request):
    if request.is_ajax() and request.method == "GET":
        response = {'random-dish-info': get_random_dish(request)}
        return JsonResponse(response)
    else:
        raise Http404

def get_random_dish(request):
    user = request.user
    dishes_id = user.choice.food.values_list('id', flat=True).order_by('id')
    rand_dishes = Food.objects.exclude(id__in=dishes_id)
    if rand_dishes.count() > 0:
        r_dish = random.choice(rand_dishes)
        return str(f'{r_dish.name}')
    else:
        return 'Nice Done! You have marked everything!'

# DRINKS --------------------------------------------------------------------------------------

def is_all_drunk(l_user):
    num_drinks = count_all_obj(Drink)
    user_num_drinks = l_user.choice.drinks.all().count()
    return num_drinks == user_num_drinks

def drink_checkbox(request):
    if request.is_ajax and request.method == "POST":
        user = request.user
        drink = Drink.objects.get(id=request.POST['drink_id'])
        if request.POST['is_drunk'] == 'true':
            user.choice.drinks.add(drink)
            response = {'is-all-drunk': is_all_drunk(user)}
        else:
            user.choice.drinks.remove(drink)
            response = {'is-all-drunk': is_all_drunk(user)}
        return JsonResponse(response)
    else:
        raise Http404

def random_drink(request):
    if request.is_ajax() and request.method == "GET":
        response = {'random-drink-info': get_random_drink(request)}
        return JsonResponse(response)
    else:
        raise Http404

def get_random_drink(request):
    user = request.user
    drinks_id = user.choice.drinks.values_list('id', flat=True).order_by('id')
    rand_drinks = Drink.objects.exclude(id__in=drinks_id)
    if rand_drinks.count() > 0:
        r_drink = random.choice(rand_drinks)
        return str(f'{r_drink.name}')
    else:
        return 'Nice Done! You have marked everything!'
