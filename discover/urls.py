from django.urls import path
from . import views

urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    path('details/', views.event_details, name='event_details'),
    path('org/', views.org, name='org_details'),
    path('register/', views.event_register, name='event_register'),
    path('dashboard/', views.dashboard, name='discover_dashboard'),
    ]
