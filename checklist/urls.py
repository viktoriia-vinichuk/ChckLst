from django.urls import path

from . import views

urlpatterns = [
    path('', views.checklists, name='checklists'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('movies/', views.MovieListView.as_view(), name='movies'),
    path('food/', views.FoodListView.as_view(), name='food'),
    path('drinks/', views.DrinkListView.as_view(), name='drinks'),
    path('stats/', views.stats, name='stats'),
]