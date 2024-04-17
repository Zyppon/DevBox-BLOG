from django.contrib import admin
from .models import BlogPost  , NewsPost
from markdownx.admin import MarkdownxModelAdmin


admin.site.register(BlogPost, MarkdownxModelAdmin)
admin.site.register(NewsPost)

