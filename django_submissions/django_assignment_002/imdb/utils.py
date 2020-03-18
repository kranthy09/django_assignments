from models import Actor, Director, Movie, Cast, Rating
import datetime


def populate_database(actors_list, movies_list, directors_list, movie_rating_list):
    """
        actors_list : is a list of dictionaries containing actor_id, name as keys
        and values.
        
        movies_list : is a list of dictionaries containing movie information
        for each movie
        
        directors_list : is list of director's name
        
        movie_rating_list : is list of dictionaries containing movie_id
        and count of each_rating]
        
    """
    for actor in actors_list:
        #creating actor object
        actor_object = Actor.objects.create(name=actor['name'],
                                    actor_id=actor['actor_id'])
    
    for director_name in directors_list:
        director_obj = Director.objects.create(name=director_name)
    
    for movie in movies_list:
        movie_obj = Movie.objects.create(name=movie['name'],
                                         movie_id = movie['movie_id'],
                                         release_date = 
                                         datetime.datetime.strptime(
                                             movie['release_date'],"%Y-%m-%d"),
                                        box_office_collection_in_crores = movie['box_office_collection_in_crores'],
                                        director = director_obj
                                        )
        
        #cast_in_movie_object storing the list of dictionaries.
        
        cast_in_movie_object = movie['actors']
        for cast in cast_in_movie_object:
            actors_in_each_movie = movie_obj.cast_set.create(actors = actor_object,
                                      through_defaults = {
                                          'role' : cast['role'],
                                          'is_debut_movie' : cast['is_debut_movie']
                                      }
                                     )
    for movie_rating in movie_rating_list:
        Rating.objects.create(movie_id = movie_rating['movie_id'],
                              rating_one_count = movie_rating['rating_one_count'],
                              rating_two_count = movie_rating['rating_two_count'],
                              rating_three_count = movie_rating['rating_three_count'],
                              rating_four_count = movie_rating['rating_four_count'],
                              rating_five_count = movie_rating['rating_five_count']
                             )
    
    return
            
        
    
def get_no_of_distinct_movies_actor_acted(actor_id):
    
    actor = Actor.objects.get(pk=actor_id)
    actor_acted_in_movies = actor.movie_set.all().distinct().count()
    
    return

def get_movies_directed_by_director(director_obj):
    
    list_of_movies_by_director = []
    for director_s_movie in director_obj.movie_set.all():
        list_of_movies_by_director.append(director_s_movie)
    
    return list_of_movies_by_director

def get_average_rating_of_movie(movie_obj):
    
    
    rating_object = Rating.objects.get(movie_id=movie_obj.movie_id)
    
    average_rating_movie = (rating_object.rating_one_count +
                            rating_object.rating_two_count +
                            rating_object.rating_three_count +
                            rating_object.rating_four_count +
                            rating_object.rating_five_count)/5
    
    return average_rating_movie

def delete_movie_rating(movie_obj):
    
    Rating.objects.get(movie_id=movie_obj.movie_id).delete()
    
    return

def get_all_actor_objects_acted_in_given_movies(movie_objs):
    
    actors_list = []
    for each_movie_object in movie_objs:
        try:
            actor_acted_in_movies = each_movie_object.actors.all()
        except:
            continue
        
        for actor in actor_acted_in_movies:
                actors_list.append(actor)
    
    return actors_list

def update_director_for_given_movie(movie_obj, director_obj):
    
    director_obj.movie_set.add(movie_obj)
    
    return

def get_distinct_movies_acted_by_actor_whose_name_contains_john():
    
    movies_list = []
    try:
        movies_queryset = Movie.objects.filter(name__contains="john").distinct()
    except:
        return movies_list
    
    for movie in movies_queryset:
        movies_list.append(movie)
    return movies_list

def remove_all_actors_from_given_movie(movie_obj):
    
    movie_obj.actors.all().delete()
    
    return

def get_all_rating_objects_for_given_movies(movie_objs):
    
    rating_objs = []
    for movie_object in movie_objs:
        try:
            rating_object = Rating.objects.get(movie_id = movie_object.movie_id)
        except:
            continue
        rating_objs.append(rating_object)
    
    return rating_objs