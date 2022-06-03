from django.contrib import admin

# Register your models here.
from .models import Genre, Movie, MovieGenre

admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(MovieGenre)