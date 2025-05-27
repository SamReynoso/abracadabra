from django.conf import settings

from django.urls import path, include
from . import views

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('billing/', views.billing, name='billing'),

]
