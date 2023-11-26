from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User


class BlogPost(models.Model):

    title = models.CharField(max_length=200)
    body = RichTextUploadingField()
   # content = models.TextField(max_length=999999999)
    date_posted = models.DateTimeField(auto_now_add=True)


    def __str__(self):

        return self.title
