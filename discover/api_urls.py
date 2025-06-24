from django.urls import path
from . import api

urlpatterns = [
        path('contact-info/', api.guest_contact_info_form, name='contact_info_form'),  
        path('team/', api.team_form, name='team_form'),
        path('team-delete/', api.team_delete, name='team_delete'),
        path('division/', api.division_form, name='division_form'),
        path('division-delete/', api.division_delete, name='division_delete'),
        path('registration-form/', api.registration_form, name='registration_form'),
        path('registration-cancel/', api.registration_cancel_or_delete, name='registration_cancel'),
        path('registration-submit', api.registration_submit, name='registration_submit'),
        path('entry-update-', api.entry_update, name='entry_update'),
        ]
