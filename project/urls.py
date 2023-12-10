from django.contrib import admin
from django.urls import path , include  ,re_path
from app.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   path('admin/', admin.site.urls),
   path('',index , name="index"),
   path('privacy/',privacy , name="privacy"),
   path('login/',login_user , name="login"),
   path('register/',register , name="register"),
   path('logout/', logout, name='logout'),
   path('add_post',create_post,name='add_post'),
   path('post/<int:post_id>/', blog_detail, name='blog_detail'),
]

urlpatterns +=  static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)

#if settings.DEBUG: 
  # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
