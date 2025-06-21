from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    path('basketball/', views.basketball, name='basketball'),
    path('event/<event_slug>/', views.event_details, name='event_details'),
    path('event-registration/', views.event_registration, name='event_registration'),
    path('org/<org_slug>/', views.org_details, name='org_details'),
    path('persona/<user_slug>/', views.persona, name='discover_persona'),

    path('workspace/', views.workspace, name='workspace'),
    path('workspace-content/', views.workspace_content, name='workspace_content'),
    path('contact-info/', views.contact_info, name='contact_info'),


    path('api/', include('discover.api_urls')),


#    path('basketball-spotlight/<page_number>/', views.basketball_spotlight, name='basketball_spotlight'),
#    path('register/<safe_slug>/', views.event_register, name='event_register'),
#    path('dashboard/', views.dashboard, name='discover_dashboard'),
#    path('persona/>', views.persona, name='discover_persona'),
#    path('basketball/load-more/', views.load_more, name='director_load_more'),
#    path('guest/contact-info/', views.contact_info, name='contact_info'),
#    path('guest/contact-info-form/', views.contact_info_form, name='contact_info_form'),
#    path('guest/teams/', views.teams, name='teams'),
#    path('guest/team-form/', views.team_form, name='team_form'),
#    path('guest/division-form/', views.division_form, name='division_form'),
#    path('guest/division-delete/<division_id>', views.division_delete, name='division_delete'),
#    path('guest/team-delete/<team_id>', views.team_delete, name='team_delete'),
#    path('clear-cookie/', views.clear_cookie, name='clear_cookie'),
    ]
