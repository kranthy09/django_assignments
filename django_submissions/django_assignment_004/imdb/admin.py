from django.contrib import admin
from .models import Movie, Actor, Director, Cast, Rating

# Register your models here.


admin.site.register(Movie)
admin.site.register(Director)
admin.site.register(Actor)
admin.site.register(Cast)
admin.site.register(Rating)