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
        
        director_object = Director.objects.create(name=movie_details['director_name'])
        
        movie_object = Movie.objects.create(director=director_object,**movie_details)
        
        
    