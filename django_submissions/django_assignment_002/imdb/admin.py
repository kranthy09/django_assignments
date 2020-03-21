from django.contrib import admin
from .models import Actor, Director, Cast, Rating, Movie

# Register your models here.

admin.site.register(Actor),
admin.site.register(Director),
admin.site.register(Cast),
admin.site.register(Rating),
admin.site.register(Movie)