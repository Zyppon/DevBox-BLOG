from django.contrib import admin
from .models import BlogPost
from markdownx.admin import MarkdownxModelAdmin


admin.site.register(BlogPost, MarkdownxModelAdmin)
# Register your models here.
#admin.site.register(BlogPost)

