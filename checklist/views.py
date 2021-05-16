from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models import Avg
'''
def checklists(request):
    return HttpResponse("Select a checklist you wish to fill in.")
'''
from checklist.models import Book, Movie, Food, Drink, Choice


def checklists(request):

    num_books = Book.objects.all().count()
    num_movies = Movie.objects.all().count()
    num_food = Food.objects.all().count()
    num_drinks = Drink.objects.all().count()

    context = {
        'num_books': num_books,
        'num_movies': num_movies,
        'num_food': num_food,
        'num_drinks': num_drinks,
    }

    return render(request, 'checklists.html', context=context)


def stats(request):

    def count_all_obj(model):
        return model.objects.all().count()

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

    # Take into account empty choices!!!
    user_num_books = user.choice.books.all().count()
    user_num_movies = user.choice.movies.all().count()
    user_num_food = user.choice.food.all().count()
    user_num_drinks = user.choice.drinks.all().count()

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

    books_percent = round(100 * less_read / users_count)
    movies_percent = round(100 * less_watched / users_count)
    food_percent = round(100 * less_ate / users_count)
    drinks_percent = round(100 * less_drank / users_count)
    
    context = {
        'user_num_books': user_num_books,
        'user_num_movies': user_num_movies,
        'user_num_food': user_num_food,
        'user_num_drinks': user_num_drinks,
        'all_books': all_books,
        'all_movies': all_movies,
        'all_food': all_food,
        'all_drinks': all_drinks,
        'books_percent': books_percent,
        'movies_percent': movies_percent,
        'food_percent': food_percent,
        'drinks_percent': drinks_percent,
    }

    return render(request, 'statistic.html', context=context)

class BookListView(generic.ListView):
    model = Book
    template_name = 'books_checklist.html'


class MovieListView(generic.ListView):
    model = Movie


class FoodListView(generic.ListView):
    model = Food


class DrinkListView(generic.ListView):
    model = Drink
