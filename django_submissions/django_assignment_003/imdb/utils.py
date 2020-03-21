from .models import *
import json
from datetime import datetime, date

def average_rating(rating_1,rating_2,rating_3,rating_4,rating_5):
    numerator = (5*rating_5 + 4 * rating_4 + 3 * rating_3 + 2 * rating_2 + 1 * rating_1)
    
    denominator = (rating_5+rating_4+rating_3+rating_2+rating_1)
    return numerator/denominator

#1

def get_movies_by_given_movie_names(movie_names):
    
    query_list = []
    for movie_name in movie_names:
        query_dict = {}
        list_movie_objects = Movie.objects.filter(name=movie_name)
        for movie_obj in list_movie_objects:
            movie_details = {
                'movie_id' : movie_obj.movie_id,
                'name': movie_obj.name
            }
            query_dict.update(movie_details)
            
            cast_of_movie_object = movie_obj.cast_set.all().values()
            value = []
            for cast in cast_of_movie_object:
                #value is list of actor details iterates each time and captures
                #the actors for each cast object
                value.append({
                    'actor' : {
                        'name' : Actor.objects.get(pk=cast['actor_id']).name,
                        'actor_id' : cast['actor_id']
                    },
                    'role' : cast['role'], #if we get morethan 2 roles for an actor
                    'is_debut_movie' : cast['is_debut_movie']
                })
            
            cast_details = {
                'cast' : value,
                'box_office_collection_in_crores' : movie_obj.box_office_collection_in_crores,
                'release_date' : movie_obj.release_date.strftime("%Y-%d-%m"),
                'director_name' : Director.objects.get(pk = movie_obj.director_id).name,
            }
            query_dict.update(cast_details)
            
            rating_obj = Rating.objects.get(movie_id=movie_obj.movie_id)
            
            #average_rating function defined above
            avg_rating = average_rating(rating_obj.rating_one_count,
                                        rating_obj.rating_two_count,
                                        rating_obj.rating_three_count,
                                        rating_obj.rating_four_count,
                                        rating_obj.rating_five_count
                                        )
                             
            total_number_of_ratings = (rating_obj.rating_one_count + rating_obj.rating_two_count +
                                      rating_obj.rating_three_count + rating_obj.rating_four_count + 
                                      rating_obj.rating_five_count)
            rating_details = {
                'average_rating' : avg_rating,
                'total_number_of_ratings' : total_number_of_ratings
            }
            query_dict.update(rating_details)
            data_query_dict_in_json = json.dumps(query_dict, indent=4)
            query_list.append(query_dict)
    return query_list

#2

def get_movies_released_in_summer_in_given_years():
    list_of_movies_names = list(Movie.objects.filter(cast__actor__name__iendswith="smith").values_list('name', flat=True))
    
    return get_movies_by_given_movie_names(list_of_movies_names)

#3

def get_movie_names_with_actor_name_ending_with_smith():
    list_of_movie_names = list(Movie.objects.filter(actor__name__endswith="smith").values_list('name', flat=True))
    return list_of_movie_names

#4

def get_movie_names_with_ratings_in_given_range():
    
    list_of_movie_names = list(Movie.objects.filter(rating__rating_five_count__gte=1000,
                                                rating__rating_five_count__lte=3000).values_list('name', flat=True))

    return list_of_movie_names

#5

def get_movie_names_with_ratings_above_given_minimum():
    
    movies_in_21st_century = list(Movie.objects.filter(
                                Q(rating__rating_five_count__gte=500) |
                                Q(rating__rating_four_count=1000) |
                                Q(rating__rating_three_count=2000) |
                                Q(rating__rating_two_count=4000) |
                                Q(rating__rating_one_count=8000),
                                release_date__year__gt=2000
                                ).values_list('name', flat=True))
    return movies_in_21st_century

#6

def get_movie_directors_in_given_year():
    
    director_names = list(Director.objects.filter(movie__release_date__year=2000).values_list('name', flat=True))
    
    return director_names

#7

def get_actor_names_debuted_in_21st_century():
    actor_names = list(Actor.objects.filter(cast__movie__release_date__year__gt=2000).values_list('name', flat=True))
    
    return actor_names

#8

def get_director_names_containing_big_as_well_as_movie_in_may():
    
    director_names = list(Director.objects.filter(movie__name__contains="big").filter(movie__release_date__month=5).values_list('name', flat=True))
    
    return director_names

#9

def get_director_names_containing_big_and_movie_in_may():
    
    director_names = list(Director.objects.filter(movie__name__contains="big", movie__release_date__month=5).values_list('name', flat=True))
    
    return director_names

#10

def reset_ratings_for_movies_in_this_year():
    
    Rating.objects.filter(movie__release_date__year=2000).update(rating_one_count=0,
                                                                 rating_two_count=0,
                                                                 rating_three_count=0,
                                                                 rating_four_count=0,
                                                                 rating_five_count=0
                                                                )
    return