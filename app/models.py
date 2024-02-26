from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class BlogPost(models.Model):

    title = models.CharField(max_length=200)
    image = CloudinaryField('image' , null=False , blank=False) 
    body = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE , blank=True , null=True)


    def __str__(self):

        return self.title

class VerificationCode(models.Model):
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

