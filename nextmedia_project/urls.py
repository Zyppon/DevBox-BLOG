from django.contrib import admin
from django.urls import path , include
from nextmedia_app.views import index , privacy , login

urlpatterns = [
    path('admin/', admin.site.urls),
   # path('', include('nextmedia_app.urls')),
   path('',index , name="index"),
   path('privacy/',privacy , name="privacy"),
   path('login/',login , name="login"),
]
