from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.models import User

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

    all_books = Book.objects.all().count()
    all_movies = Movie.objects.all().count()
    all_food = Food.objects.all().count()
    all_drinks = Drink.objects.all().count()
    '''
    users = User.objects.all()

    c = []
    for i in users:
        read = i.choice.books.all().count()
        c.append(read)
    aver_read = sum(c)/len(c)
    '''
    from django.db.models import Count
    from django.db.models import Avg
    #countt = User.objects.annotate(num_books=Count('choice__books'))[0].num_books
    #users.objects.choice.all().aggregate(Avg('price'))
    users = User.objects.annotate(num_books=Count('choice__books'))
    users_count = users.count()

    c = 0
    for i in users:
        read = i.num_books
        c += read
    aver_read = c/users_count

    user = request.user

    num_books = user.choice.books.all().count()
    num_movies = user.choice.movies.all().count()
    num_food = user.choice.food.all().count()
    num_drinks = user.choice.drinks.all().count()
    
    context = {
        'num_books': num_books,
        'num_movies': num_movies,
        'num_food': num_food,
        'num_drinks': num_drinks,
        'all_books': all_books,
        'all_movies': all_movies,
        'all_food': all_food,
        'all_drinks': all_drinks,
        'aver_read': aver_read,
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


class UserBooksChoice(generic.ListView):
    queryset = Choice.objects.select_related('user')
    template_name = 'books_checklist.html'
