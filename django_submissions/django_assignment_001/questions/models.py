from django.db import models


# Create your models here.


class Question(models.Model):
    text = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return "{}-{}".format(self.text, self.answer)

# class Person(models.Model):
#     SHIRT_SIZES = (
#         ('S', 'Small'),
#         ('M', 'Medium'),
#         ('L', 'Large'),
#         )
