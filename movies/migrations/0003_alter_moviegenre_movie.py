# Generated by Django 4.0.4 on 2022-06-02 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_moviegenre_remove_movie_genre_movie_genre_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moviegenre',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movie', to='movies.movie'),
        ),
    ]