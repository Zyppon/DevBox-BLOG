from django.db import models


from django.contrib.auth.models import User


class BlogPost(models.Model):

    title = models.CharField(max_length=200)

    content = models.TextField(max_length=999999999)

   # author = models.ForeignKey(User, on_delete=models.CASCADE)

    date_posted = models.DateTimeField(auto_now_add=True)


    def __str__(self):

        return self.title
