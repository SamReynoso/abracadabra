from django.contrib import admin
from django.urls import path
from django.urls import include


urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('persona/', include('persona.urls')),
    path('accounts/', include('allauth.urls')),
    path('app/', include('app.urls')),
    path('info/', include('info.urls')),
    path('discover/', include('discover.urls')),
    path('gameday/', include('gameday.urls')),
]
