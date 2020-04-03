from .models import Movie, Actor, Director, Rating, Cast
from django.db.models import Avg, Sum, Max, Min, Count, Q


#1
def get_average_box_office_collections():
    try:
        avg_box_office_cllections = Movie.objects.aggregate(avg_box_office_cllections=Avg('box_office_collection_in_crores'))
        return round(avg_box_office_cllections['avg_box_office_cllections'],3)
    except:
        return 0


#2
def get_movies_with_distinct_actors_count():
    
    movies = Movie.objects.annotate(actors_count = Count('cast__actor', distinct=True))
    
    return list(movies)


#3
def get_male_and_female_actors_count_for_each_movie():
    
    movie_instances_returns_male_female_actors_count = Movie.objects.annotate(
                    male_actors_count=Count('cast__actor', filter=Q(cast__actor__gender='MALE'), distinct=True),
                female_actors_count=Count('cast__actor', filter=Q(cast__actor__gender='FEMALE'), distinct=True)
                                                                      )
    return list(movie_instances_returns_male_female_actors_count)
    

#4
def get_roles_count_for_each_movie():
    
    movies_with_distinct_roles_count = Movie.objects.annotate(roles_count = Count('cast__role', distinct=True))
    
    return list(movies_with_distinct_roles_count)


#5
def get_role_frequency():
    
    casts = Cast.objects.values('role').annotate(actors_count=Count('actor', distinct=True))
    role_dict = {}
    
    for cast in casts:
        role_dict.update({cast['role']:cast['actors_count']})
    
    return role_dict
    

#6
def get_role_frequency_in_order():
    
    from collections import defaultdict
    
    casts_order_by = Cast.objects.values('role').annotate(actors_count=Count('actor')).order_by('movie__release_date')
    d = defaultdict(int)
    for cast in casts_order_by:
        d[cast['role']] += cast['actors_count']
    
    return list(d.items())


#7
def get_no_of_movies_and_distinct_roles_for_each_actor():
    
    actors_with_no_movies_roles_acted = Actor.objects.annotate(movies_count=Count('cast__movie', distinct=True), roles_count=Count('cast__role', distinct=True))
    
    return list(actors_with_no_movies_roles_acted)


#8
def get_movies_with_atleast_forty_actors():
    
    movies_with_atleast_forty_actors = Movie.objects.annotate(actors_count=Count('cast__actor', distinct=True)).filter(actors_count__gte=40)
    
    return movies_with_atleast_forty_actors


#9
def get_average_no_of_actors_for_all_movies():
    try:
        avg_no_of_actors = Movie.objects.annotate(actors_count=Count('cast__actor')).aggregate(avg_no_of_actors=Avg('actors_count'))
        return round(avg_no_of_actors['avg_no_of_actors'],3)
    except:
        return 0