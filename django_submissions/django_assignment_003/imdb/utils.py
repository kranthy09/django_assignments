from .models import *
import json
from datetime import datetime, date

def avg_rating_function(rating_5,rating_4,rating_3,rating_2,rating_1):
    numerator = (5*rating_5 + 4 * rating_4 + 3 * rating_3 + 2 * rating_2 + 1 * rating_1)
    
    denominator = (rating_5+rating_4+rating_3+rating_2+rating_1)
    try:
        result = numerator/denominator
    except:
        result = 0
    return result


#1

def get_movies_by_given_movie_names(movie_names):
    query_result = []
    
    for movie_name in movie_names:
        movie_objects_related_to_movie_name = Movie.objects.filter(name=movie_name)
        #print(movie_objects_related_to_movie_name)
        query_each_movie = {}
        for movie_obj in movie_objects_related_to_movie_name:
            query_each_movie = {
                    'movie_id' : movie_obj.movie_id,
                    'name' : movie_obj.name
            }
            
            cast_crew = Cast.objects.filter(movie__movie_id=movie_obj.movie_id)
            value = []
            for each_cast in cast_crew:
                value.append({
                        'actor' : {
                                    'name' : Actor.objects.get(pk=each_cast.actor_id).name,
                                    'actor_id' : each_cast.actor_id
                                },
                        'role' : each_cast.role,
                        'is_debut_movie' : each_cast.is_debut_movie
                })
            
            query_each_movie['cast'] = value
            
            query_each_movie["box_office_collection_in_crores"]: movie_obj.box_office_collection_in_crores
            query_each_movie["release_date"] : str(movie_obj.release_date)
            query_each_movie["director_name"]: movie_obj.director.name
            
            #rating
            
            try:
                rating = Rating.objects.get(rating__movie_id=movie_obj.movie_id)
            except:
                rating_1 = 0
                rating_2 = 0
                rating_3 = 0
                rating_4 = 0
                rating_5 = 0
            else:
                rating_1 = movie_obj.rating.rating_one_count
                rating_2 = movie_obj.rating.rating_two_count
                rating_3 = movie_obj.rating.rating_three_count
                rating_4 = movie_obj.rating.rating_four_count
                rating_5 = movie_obj.rating.rating_five_count
            
            average_rating = avg_rating_function(rating_1, rating_2, rating_3,
                                                 rating_4, rating_5)
            
            total_number_of_ratings = rating_1 + rating_2 + rating_3 + rating_4 + rating_5
            
            query_each_movie['average_rating'] = average_rating
            query_each_movie['total_number_of_ratings'] = total_number_of_ratings
            query_result.append(query_each_movie)
    return query_result
        

#2

def get_movies_released_in_summer_in_given_years():
    list_of_movies_ids = list(Movie.objects.filter(release_date__month__in=[5,6,7], 
                                                   release_date__year__gt=2005,
                                                   release_date__year__lt=2010).values_list('movie_id', flat=True))
    
    return get_movies_by_given_movie_names(list_of_movies_ids)

#3

def get_movie_names_with_actor_name_ending_with_smith():
    list_of_movie_names = list(Movie.objects.filter(actors__name__iendswith="smith").distinct().values_list('name', flat=True))
    return list_of_movie_names

#4

def get_movie_names_with_ratings_in_given_range():
    
    list_of_movie_names = list(Movie.objects.filter(rating__rating_five_count__range=(1000,3000)).values_list('name', flat=True))

    return list_of_movie_names

#5

def get_movie_names_with_ratings_above_given_minimum():
    
    movies_in_21st_century = list(Movie.objects.filter(
                                Q(rating__rating_five_count__gte=500) |
                                Q(rating__rating_four_count__gte=1000) |
                                Q(rating__rating_three_count__gte=2000) |
                                Q(rating__rating_two_count__gte=4000) |
                                Q(rating__rating_one_count__gte=8000),
                                release_date__year__gt=2000
                                ).values_list('name', flat=True))
    return movies_in_21st_century

#6

def get_movie_directors_in_given_year():
    
    director_names = list(Director.objects.filter(movie__release_date__year=2000).distinct().values_list('name', flat=True))
    
    return director_names

#7

def get_actor_names_debuted_in_21st_century():
    actor_names = list(Actor.objects.filter(cast__is_debut_movie=True).distinct().values_list('name', flat=True))
    
    return actor_names

#8

def get_director_names_containing_big_as_well_as_movie_in_may():
    
    director_names = list(Director.objects.filter(movie__name__contains="big").filter(movie__release_date__month=5).distinct().values_list('name', flat=True))
    
    return director_names

#9

def get_director_names_containing_big_and_movie_in_may():
    
    director_names = list(Director.objects.filter(movie__name__contains="big", movie__release_date__month=5).distinct().values_list('name', flat=True))
    
    return director_names

#10

def reset_ratings_for_movies_in_this_year():
    
    movie_rating = Movie.objects.filter(release_date__year=2000)
    for movie in movie_rating:
        try:
            Rating.objects.get(movie=movie)
        except Rating.DoesNotExist:
            pass
        else:
            movie.rating.rating_five_count = 0
            movie.rating.rating_two_count=0
            movie.rating.rating_three_count=0
            movie.rating.rating_four_count=0
            movie.rating.rating_one_count=0
            movie.rating.save()
    return