from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Author, B_Genre, Book, M_Genre, Movie, F_Kind, Food, Ingredient, D_kind, Drink, Choice, Statistic

# GENERAL -------------------------------------------------------------------------------------

class HideModelAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}

admin.site.register(Statistic, HideModelAdmin)

# BOOKS Checklist -----------------------------------------------------------------------------

admin.site.register(Author, HideModelAdmin)

admin.site.register(B_Genre, HideModelAdmin)

@admin.register(Book)
class MyModelAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('order','title', 'display_author','display_genre')
    list_display_links = ('order','title')
    filter_horizontal = ('author','genre')

class BookInline(admin.TabularInline):
    model = Book

class AuthorAdmin(admin.ModelAdmin):
    inlines = [
        BookInline,
    ]

# MOVIES Checklist ----------------------------------------------------------------------------

admin.site.register(M_Genre, HideModelAdmin)

@admin.register(Movie)
class MyModelAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('order','title', 'year','display_genre')
    list_display_links = ('order','title')
    filter_horizontal = ('genre',)

class MovieInline(admin.TabularInline):
    model = Movie

class AuthorAdmin(admin.ModelAdmin):
    inlines = [
        MovieInline,
    ]

# FOOD Checklist ------------------------------------------------------------------------------

admin.site.register(Ingredient, HideModelAdmin)

admin.site.register(F_Kind, HideModelAdmin)

@admin.register(Food)
class MyModelAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('order','name', 'country', 'display_kind')
    list_display_links = ('order','name')
    filter_horizontal = ('food_kinds', 'food_ingredients')

class FoodInline(admin.TabularInline):
    model = Food

class AuthorAdmin(admin.ModelAdmin):
    inlines = [
        FoodInline,
    ]

# DRINKS Checklist ----------------------------------------------------------------------------

admin.site.register(D_kind, HideModelAdmin)

@admin.register(Drink)
class MyModelAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('order','name', 'country','alcohol','display_kind')
    list_display_links = ('order','name')
    filter_horizontal = ('drink_kinds', 'drink_ingredients')

class DrinkInline(admin.TabularInline):
    model = Drink

class AuthorAdmin(admin.ModelAdmin):
    inlines = [
        DrinkInline,
    ]

# User Profile Checklists ---------------------------------------------------------------------

class ChoicesInline(admin.StackedInline):    
    model = Choice
    can_delete = False
    verbose_name_plural = 'Choices'
    fk_name = 'user'
    filter_horizontal = ('books','movies','food','drinks')

class CustomUserAdmin(UserAdmin):
    inlines = (ChoicesInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)