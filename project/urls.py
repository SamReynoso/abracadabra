from django.contrib import admin
from django.urls import path
from django.urls import include


urlpatterns = [
    path('', include('marketing.urls')),
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')),
    path('info/', include('info.urls')),
    path('user/', include('user.urls')),
]
