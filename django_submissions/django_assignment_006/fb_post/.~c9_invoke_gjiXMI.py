from django.db import models

# Create your models here.

class User(models.Model):
    
    name = models.TextField(max_length=100, null=False)
    profile_pic = models.TextField(null=False)


class Post(models.Model):
    
    content = models.TextField(max_length=1000, null=False)
    posted_at = models.DateField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    
    content = models.TextField(max_length=1000)
    commented_at = models.DateField()
    commented_by = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE)

class Reaction(models.Model):
    
    