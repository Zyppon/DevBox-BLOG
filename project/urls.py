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
   path('add_post/',create_post,name='add_post'),
   path('post/<int:post_id>/', blog_detail, name='blog_detail'),
   path('settings/' , user_settings_panel , name='user_settings'),
   path('activate/<uidb64>/<token>/', activate_account, name='activate_account'),
  # path('reset_password/<uidb64>/<token>/' , reset_password , name='reset_password')
   path('reset_password/' , reset_password , name='reset_password'),
   path('reset_password_confirm/<uidb64>/<token>/' , reset_password_confirm , name='reset_password_confirm'),
   path('reset_password_done/', reset_password_done, name='reset_password_done'),
   path('courses/' , courses_download , name="courses_download")

]

urlpatterns +=  static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)

#if settings.DEBUG: 
  # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
