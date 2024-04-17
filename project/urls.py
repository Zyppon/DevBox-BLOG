from django.contrib import admin
from django.urls import path , include  ,re_path 
from app.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   path('admin/', admin.site.urls),
   path('',index , name="index"),
   path('about_us/' , about_us , name="about_us"),
   path('news/' , news , name="news"),
   path('contact/',contact , name="contact"),
   path('login/',login_user , name="login"),
   path('register/',register , name="register"),
   path('logout/', logout, name='logout'),
   path('add_post/',create_post,name='add_post'),
   path('update_post/', update_post , name='update_post'),
   path('post/<int:post_id>/', blog_detail, name='blog_detail'),
   path('edit_post/<int:post_id>/', edit_post_view, name='edit_post_view'),
   path('settings/' , user_settings , name='user_settings'),
   path('settings/changepassword/' , change_password , name='change_password'),
   path('activate/<uidb64>/<token>/', activate_account, name='activate_account'),
  # path('reset_password/<uidb64>/<token>/' , reset_password , name='reset_password')
   path('reset_password/' , reset_password , name='reset_password'),
   path('reset_password_confirm/<uidb64>/<token>/' , reset_password_confirm , name='reset_password_confirm'),
   path('reset_password_done/', reset_password_done, name='reset_password_done'),
   path('courses/' , courses_download , name="courses_download"),
   path('confirm/<uidb64>/<token>/', confirm_email, name='confirm_email'),


]

urlpatterns +=  static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)

#if settings.DEBUG: 
  # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
