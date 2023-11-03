from django.contrib import admin
from django.urls import path , include
from nextmedia_app.views import *




urlpatterns = [
    path('admin/', admin.site.urls),
   # path('', include('nextmedia_app.urls')),
   path('',index , name="index"),
   path('privacy/',privacy , name="privacy"),
   path('login/',login_user , name="login"),
   #path('accounts/', include('django.contrib.auth.urls')),
   path('register/',register , name="register"),
  path('logout/', logout, name='logout'),
   
]
