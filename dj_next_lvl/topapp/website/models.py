from django.db import models

# Create your models here.

from django.db import models

class Blog(models.Model):
    
    #table columns
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name

class Author(models.Model):
    
    #table columns
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Entry(models.Model):
    
    #keys associated with the tables
    authors = models.ManyToManyField(Author)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    
    #table columns
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    number_of_comments = models.IntegerField()
    number_of_pingbacks = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self):
        return self.headline


class EntryDetail(models.Model):
    entry = models.OneToOneField(Entry, on_delete=models.CASCADE)
    details = models.TextField()
    
"""

entry = Entry.objects.create(blog_pk=, 
                             headline = "this is entry 1",
                             body_text = "instance of Entry Class",
                             pub_date = date(2020,2,3),
                             mod_date = date(2020, 1,4),
                             number_of_comments = 5,
                             number_of_pingbacks = 7
                            )

bod.entry_set.create( 
                             headline = "this is entry 1",
                             body_text = "instance of Entry Class",
                             pub_date = date(2020,2,3),
                             mod_date = date(2020, 1,4),
                             number_of_comments = 5,
                             number_of_pingbacks = 7
                            )
"""

"""
*status*

learnt till updating(save) a foreign key of a table.

continue from ManyToManyField;
"""