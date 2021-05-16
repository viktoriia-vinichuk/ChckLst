from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required

from . import views

urlpatterns = [
    path('', views.checklists, name='checklists'),
    path('books/', login_required(views.BookListView.as_view()), name='books'),
    path('movies/', login_required(views.MovieListView.as_view()), name='movies'),
    path('food/', login_required(views.FoodListView.as_view()), name='food'),
    path('drinks/', login_required(views.DrinkListView.as_view()), name='drinks'),
    path('stats/', login_required(views.stats), name='stats'),
    path('random_book/', views.random_book, name='random_book'),
    path('book_checkbox/', views.book_checkbox, name='book_checkbox'),
]