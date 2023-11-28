from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django_summernote.fields import SummernoteTextField
from markdownx.models import MarkdownxField

class BlogPost(models.Model):

    title = models.CharField(max_length=200)
    body = RichTextUploadingField()
   # body = RichTextUploadingField()
   # body = SummernoteTextField()
    body = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)


    def __str__(self):

        return self.title
