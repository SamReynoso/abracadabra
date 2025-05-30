from django.contrib import admin
from django.urls import path
from django.urls import include


urlpatterns = [
    path('', include('marketing.urls')),
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')),
    path('info/', include('info.urls')),
    path('persona/', include('persona.urls')),
    path('discover/', include('discover.urls')),
    path('gameday/', include('gameday.urls')),
]
