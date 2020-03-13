from models import Actor, Director, Movie, Cast, Rating
from datetime import date
def populate_database(actors_list, movies_list, directors_list, movie_rating_list):
    for actor in actors_list:
        actor_object = Actor.objects.create(name=actor['name'], actor_id=actor['actor_id'])
    
    for movie in movies_list:
        movie_obj = Movie.objects.create(name=movie['name'],
                                         movie_id = movie['movie_id'],
                                         box_office_collection_in_crores = 
                                         float(movie['box_office_collection_in_crores']),
                                         release_date = date(",".join(list(map(int, movie['release_date'].split('-')))))
                                        )
        for actor in movie['actors']:
            movie_obj.cast_set.create(actor_id=actor['actor_id'],
                                      through_defaults={'role':actor['role'],
                                                        'is_debut_movie':actor['is_debut_movie']
                                                        }
                                     )
        
        
    
    
    """
    :param actors_list:[
        {
            "actor_id": "actor_1",
            "name": "Actor 1"
        }
    ]
    :param movies_list: [
        {
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
    ]
    :param directors_list: [
        "Director 1"
    ]
    :param movie_rating_list: [
        {
            "movie_id": "movie_1",
            "rating_one_count": 4,
            "rating_two_count": 4,
            "rating_three_count": 4,
            "rating_four_count": 4,
            "rating_five_count": 4
        }
    ]
"""
