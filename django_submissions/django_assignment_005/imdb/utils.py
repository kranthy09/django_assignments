from .models import Actor, Movie, Cast, Director, Rating
from datetime import datetime
from django.db.models import Prefetch

def average_rating(rating_1, rating_2, rating_3, rating_4, rating_5):
    
    numerator = 1*rating_1 + 2*rating_2 + 3*rating_3 + 4*rating_4 + 5*rating_5
    denominator = rating_1 + rating_2 + rating_3 + rating_4 + rating_5
    
    try:
        result = numerator/denominator
    except:
        result = 0
    return result

#Task 1

def populate_database(actors_list, movies_list, directors_list, movie_rating_list):
    
    Actor.objects.bulk_create([
        Actor(actor_id=actor['actor_id'], name=actor['name'], gender=actor['gender']) 
        for actor in actors_list
        ])
    
    Director.objects.bulk_create([
        Director(name=director_name) for director_name in directors_list
        ])
        
    directors = Director.objects.all()
    
    Movie.objects.bulk_create([
        Movie(movie_id=movie['movie_id'],
              name=movie['name'],
              box_office_collection_in_crores=movie['box_office_collection_in_crores'],
              release_date=datetime.strptime(movie['release_date'],"%Y-%m-%d"),
              director_id=director.id
            ) for movie in movies_list 
              for director in directors if director.name==movie['director_name'] 
        ])
    
    Cast.objects.bulk_create([ 
        Cast(movie_id=movie['movie_id'],
              actor_id=actor['actor_id'],
              role=actor['role'],
              is_debut_movie=actor['is_debut_movie'])
              for movie in movies_list for actor in movie['actors']
              ])
    
    Rating.objects.bulk_create([
        Rating(movie_id=rating['movie_id'],
               rating_one_count=rating['rating_one_count'],
               rating_two_count=rating['rating_two_count'],
               rating_three_count=rating['rating_three_count'],
               rating_four_count=rating['rating_four_count'],
               rating_five_count=rating['rating_five_count'])
               for rating in movie_rating_list
        ])
    
    return

#Task 2

def remove_all_actors_from_given_movie(movie_object):
    
    movie_object.actors.clear()
    
    return

#Task 3

def get_all_rating_objects_for_given_movies(movie_objs):
    
    ratings_list = list(Rating.objects.filter(movie__in=movie_objs))
    
    return ratings_list

#Task 4

def get_movies_by_given_movie_names(movie_names):
    
    movies = Movie.objects.filter(name__in=movie_names).select_related('director', 'rating').prefetch_related(Prefetch('actors__cast_set', to_attr='cast_in_this_movie'))
    
    movie_dict = {}
    for movie in movies:
        movie_dict['movie_id'] = movie.movie_id
        movie_dict['name'] = movie.name
        
        cast_list = []
        
        for actor in movie.actors.all():
            cast_dict = {}
            actor_dict = {}
            
            actor_dict['name'] = actor.name
            actor_dict['actor_id'] = actor.actor_id
            
            cast_dict['actor'] = actor_dict
            for cast in actor.cast_in_this_movie:
                cast_dict['role'] = cast.role
                cast_dict['is_debut_movie'] = cast.is_debut_movie
                
                cast_list.append(cast_dict)
                
        movie_dict['cast'] = cast_list
        
        movie_dict['box_office_collection_in_crores'] = movie.box_office_collection_in_crores
        
        movie_dict['release_date'] = str(movie.release_date)
        
        movie_dict['director_name'] = movie.director.name
        
        if movie.rating:
            movie_dict['average_rating'] = average_rating(movie.rating.rating_one_count, 
                                                          movie.rating.rating_two_count,
                                                          movie.rating.rating_three_count,
                                                          movie.rating.rating_four_count,
                                                          movie.rating.rating_five_count
                                                         )
        else:
            movie_dict['average_rating'] = 0
        
        movie_dict['total_number_of_ratings'] = movie.rating.rating_one_count+movie.rating.rating_two_count+movie.rating.rating_three_count+movie.rating.rating_four_count+movie.rating.rating_five_count
        
    return movie_dict

#Task 5

def get_all_actor_objects_acted_in_given_movies(movie_objs):
    pass