from django.urls import path
from . import views

urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    path('basketball/', views.basketball, name='basketball'),
    path('details/', views.event_details, name='event_details'),
    path('org/', views.org, name='org_details'),
    path('register/', views.event_register, name='event_register'),
    path('dashboard/', views.dashboard, name='discover_dashboard'),
    path('persona/', views.persona, name='director_persona'),

    path('basketball/load-more/', views.load_more, name='director_persona'),
    ]
