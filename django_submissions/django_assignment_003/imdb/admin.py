from django.contrib import admin
from .models import Actor, Movie, Cast, Director, Rating
# Register your models here.

admin.site.register(Actor)
admin.site.register(Movie)
admin.site.register(Cast)
admin.site.register(Director)
admin.site.register(Rating)