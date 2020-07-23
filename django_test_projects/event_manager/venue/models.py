from django.db import models

# Create your models here.


from django.db import models

# Create your models here.

class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=120)
    address = models.CharField(max_length=300, blank=True)
    zip_code = models.CharField('Zip/Post Code', max_length=12, blank=True)
    phone = models.CharField('Contact Phone', max_length=20, blank=True)
    web = models.URLField('Web Address', blank=True)
    email_address = models.EmailField('Email Address', blank=True)

    def __str__(self):
        return self.name


class MyclubUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30,  blank=True)
    email = models.EmailField('User Email',  blank=True)
    def __str__(self):
        return self.first_name + " " + self.last_name


class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField('Event Date',auto_now=True)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    manager = models.CharField(max_length = 60, blank=True)
    attendees = models.ManyToManyField(MyclubUser)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
