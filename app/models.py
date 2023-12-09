from django.db import models
from django.contrib.auth.models import User

class BlogPost(models.Model):

    title = models.CharField(max_length=200)
    body = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)


    def __str__(self):

        return self.title
