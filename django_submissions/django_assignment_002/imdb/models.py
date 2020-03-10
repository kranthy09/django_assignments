from django.db import models

# Create your models here.

class Movie(models.Model):
    
    name = models.CharField(max_length=100)
    movie_id = models.CharField(max_length=100)
    release_date = models.DateField()
    box_office_collection_in_crores = models.DecimalField(decimal_places=2)
#onyl one director directs a movie


class Actor(models.Model):
    actor_id  = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    movie = models.ManyToManyField(Movie, through="Cast")
#ActorMovies


class Director(models.Model):
    name = models.CharField(unique=True)
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE)


class Cast(models.Model):
    #intermediary table for Actor and Movie
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    is_debut_movie = models.BooleanField(default=False)

class Rating(models.Model):
    RATING_CHOICES = [
            (1, 'rating_one_count'),
            (2, 'rating_two_count'),
            (3, 'rating_three_count'),
            (4, 'rating_four_count'),
            (5, 'rating_five_count'),
        ]
    rating = models.IntegerField(max_length=1, choices=RATING_CHOICES, default=0)
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE)