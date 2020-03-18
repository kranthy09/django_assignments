from models import Actor, Director, Movie, Cast, Rating

from datetime import datetime

def populate_database(actors_list, movies_list, directors_list, movie_rating_list):
    for actor_details in actors_list:
        actor_object = Actor.objects.create(name=actor_details['name'],
                                            actor_id=actor_details['actor_1']
                                            )
    
    for director_name in directors_list:
        director_object = Director.objects.create(name=director_name)
    
    for movie_details in movies_list:
        
        director_of_movie = {'director_name' : movie_details['director_name']}
        director_object = Director.objects.create(name=movie_details['director_name'])
        
        actors_in_movie = {'actors' : movie_details['actors']}
        
        del movie_details['actors']
        del movie_details['director_name']
        movie_object = Movie.objects.create(director=director_object,**movie_details)
        
        for actors_details in actors_in_movie['actors']:
            actor_object = Actor.objects.get(pk=actor_details['actor_id'])
            
            del actors_details['actor_id']
            cast_object = Cast.objects.create(movie=movie_object, actor=actor_object,
                                                **actor_details)
        

"""
 
movies_list = {
            "movie_id": "movie_1",
            "name": "Movie 1",
            "actors": [
                {
                    "actor_id": "actor_1",
                    "role": "hero",
                    "is_debut_movie": False
                }
            ],
            "box_office_collection_in_crores": "12.3",
            "release_date": "2020-3-3",
            "director_name": "Director 1"
        }
"""