from django.urls import path
from . import views

urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    path('basketball/', views.basketball, name='basketball'),
    path('basketball-spotlight/<page_number>/', views.basketball_spotlight, name='basketball_spotlight'),
    path('event/<event_slug>/', views.event_details, name='event_details'),
    path('org/<org_slug>/', views.org_details, name='org_details'),
    path('register/<safe_slug>/', views.event_register, name='event_register'),
    path('dashboard/', views.dashboard, name='discover_dashboard'),
    path('persona/<user_slug>/', views.persona, name='discover_persona'),
    #path('persona/>', views.persona, name='discover_persona'),

    path('basketball/load-more/', views.load_more, name='director_load_more'),
    path('workspace/', views.workspace, name='workspace'),
    path('guest/contact-info/', views.contact_info, name='contact_info'),
    path('guest/contact-info-form/', views.contact_info_form, name='contact_info_form'),
    path('guest/teams/', views.teams, name='teams'),
    path('guest/team-form/', views.team_form, name='team_form'),
    path('guest/division-form/', views.division_form, name='division_form'),

    path('clear-cookie/', views.clear_cookie, name='clear_cookie'),
    ]
