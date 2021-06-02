from django.db import models
from django.contrib.auth.models import User
from django.db.models import fields
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField

# BOOKS Models --------------------------------------------------------------------------------

class Author(models.Model):
   name = models.CharField(max_length=100)
   def __str__(self):
      return self.name
   class Meta(object):
      ordering = ['name']

class B_Genre(models.Model):
   genre = models.CharField(max_length=100)
   def __str__(self):
      return self.genre
   class Meta(object):
      ordering = ['genre']

class Book(models.Model):

   order = models.PositiveIntegerField(default=0)
   title = models.CharField(max_length=200)
   author = models.ManyToManyField(Author)
   genre = models.ManyToManyField(B_Genre, blank=True)

   def __str__(self):
      return self.title

   class Meta(object):
      ordering = ['order']

   def display_author(self):
      return ', '.join(author.name for author in self.author.all())
   display_author.short_description = 'Author'

   def display_genre(self):
      return ', '.join(genre.genre for genre in self.genre.all()[:3])
   display_genre.short_description = 'Genre'

# MOVIES Models --------------------------------------------------------------------------------

class M_Genre(models.Model):
   genre = models.CharField(max_length=100)
   def __str__(self):
      return self.genre
   class Meta(object):
      ordering = ['genre']

class Movie(models.Model):

   order = models.PositiveIntegerField(default=0, blank=False, null=False)
   title = models.CharField(max_length=200)
   year = models.IntegerField()
   genre = models.ManyToManyField(M_Genre, blank=True)

   def __str__(self):
      return self.title

   class Meta(object):
      ordering = ['order']

   def display_genre(self):
      return ', '.join(genre.genre for genre in self.genre.all()[:3])
   display_genre.short_description = 'Genre'

# FOOD Models ----------------------------------------------------------------------------------

class Ingredient(models.Model):
   ingredient = models.CharField(max_length=100)
   def __str__(self):
      return self.ingredient
   class Meta(object):
      ordering = ['ingredient']

class F_Kind(models.Model):
   food_kind = models.CharField(max_length=100)
   def __str__(self):
      return self.food_kind
   class Meta(object):
      ordering = ['food_kind']

class Food(models.Model):

   order = models.PositiveIntegerField(default=0, blank=False, null=False)
   name = models.CharField(max_length=200)
   country = CountryField(blank=True)
   food_kinds = models.ManyToManyField(F_Kind, blank=True)
   food_ingredients = models.ManyToManyField(Ingredient, blank=True)

   def __str__(self):
      return self.name
    
   class Meta(object):
      ordering = ['order']
      verbose_name = 'Food'
      verbose_name_plural = 'Food'

   def display_kind(self):
      return ', '.join(food_kinds.food_kind for food_kinds in self.food_kinds.all()[:3])
   display_kind.short_description = 'Kind'

# DRINKS Models --------------------------------------------------------------------------------

class D_kind(models.Model):
   drink_kind = models.CharField(max_length=100)
   def __str__(self):
      return self.drink_kind
   class Meta(object):
      ordering = ['drink_kind']

class Drink(models.Model):

   order = models.PositiveIntegerField(default=0, blank=False, null=False)
   name = models.CharField(max_length=200)
   alcohol = models.BooleanField(default=False)
   country = CountryField(blank=True)
   drink_kinds = models.ManyToManyField(D_kind, blank=True)
   drink_ingredients = models.ManyToManyField(Ingredient, blank=True)

   def __str__(self):
      return self.name

   class Meta(object):
      ordering = ['order']

   def display_kind(self):
      return ', '.join(drink_kinds.drink_kind for drink_kinds in self.drink_kinds.all()[:3])
   display_kind.short_description = 'Type'

# User Profile Models -------------------------------------------------------------------------

class Choice(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   books = models.ManyToManyField(Book, blank=True)
   movies = models.ManyToManyField(Movie, blank=True)
   food = models.ManyToManyField(Food, blank=True)
   drinks = models.ManyToManyField(Drink, blank=True)
   
   def __str__(self):
      return 'User_choice'

@receiver(post_save, sender=User)
def create_choice(sender, instance, created, **kwargs):
   if created:
      Choice.objects.create(user=instance)

# Stats Model ---------------------------------------------------------------------------------

class Statistic(models.Model):
   user_id = models.OneToOneField(User, on_delete=models.CASCADE)
   num_books = models.PositiveIntegerField(default=0, blank=False, null=False)
   num_movies = models.PositiveIntegerField(default=0, blank=False, null=False)
   num_food = models.PositiveIntegerField(default=0, blank=False, null=False)
   num_drinks = models.PositiveIntegerField(default=0, blank=False, null=False)

   def __str__(self):
      return str(self.user_id.username)