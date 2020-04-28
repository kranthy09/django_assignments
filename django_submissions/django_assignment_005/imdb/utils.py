from .models import Actor, Movie, Cast, Director, Rating
from datetime import datetime

def populate_database(actors_list, movies_list, directors_list, movie_rating_list):
    
    Actor.objects.bulk_create([
        Actor(actor_id=actor['actor_id'], name=actor['name'], gender=actor['gender']) 
        for actor in actors_list
        ])
    
    Director.objects.bulk_create([
        Director(name=director_name) for director_name in directors_list
        ])
    
    Movie.objects.bulk_create([
        Movie(movie_id=movie['movie_id'],
              name=movie['name'],
              box_office_collection_in_crores=movie['box_office_collection_in_crores'],
              release_date=datetime.strptime(movie['release_date'],"%Y-%m-%d"),
              director=Director.objects.get(name=movie['director_name'])
            ) for movie in movies_list
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