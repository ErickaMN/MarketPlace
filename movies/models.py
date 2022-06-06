from django.db import models

# Create your models here.
from rest_framework.authtoken.admin import User

import user
from user.models import MyUser


class Genre (models.Model):
     slug = models.SlugField(max_length=100, primary_key=True)
     name = models.CharField(max_length=150, unique=True)

     def __str__(self):
         return self.name


class MovieGenre(models.Model):
    movie = models.ForeignKey('Movie', related_name='movie', on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, related_name='genre', on_delete=models.RESTRICT)


class Movie (models.Model):
    #title = models.ForeignKey(MyUser, related_name='movies')
    genre = models.ManyToManyField(Genre, through=MovieGenre)
    title = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to='images', null=True, blank=True)
    video = models.FileField(upload_to='videos', null=True, blank=True)

    def __str__(self):
        return self.title


class Comment (models.Model):
    owner = models.ForeignKey(MyUser, related_name='comments', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self)->str:
        return f'{self.owner}->{self.movie}->{self.created_at}'


class Likes (models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey('user.MyUser', on_delete=models.CASCADE, related_name='liked')

    class Meta:
        unique_together = ['movie', 'user']


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='favorites')



