from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('accounts.urls')),
    path('',include('music.urls')),
    path('game/', include('game.urls')),
  
]
