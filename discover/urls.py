from django.urls import path
from . import views

urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    path('basketball/', views.basketball, name='basketball'),
    path('event/<event_slug>', views.event_details, name='event_details'),
    path('org/<org_slug>', views.org_details, name='org_details'),
    path('register/', views.event_register, name='event_register'),
    path('dashboard/', views.dashboard, name='discover_dashboard'),
    path('persona/<user_slug>', views.persona, name='discover_persona'),
    #path('persona/>', views.persona, name='discover_persona'),

    path('basketball/load-more/', views.load_more, name='director_load_more'),
    ]
