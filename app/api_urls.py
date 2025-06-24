from django.urls import path
from . import api

urlpatterns = [
    path("event-form", api.event_form, name="event_form"),
    path("event-poster-select", api.event_poster_select, name="event_poster_select"),
    path("event-poster-accept", api.event_poster_accept, name="event_poster_accept"),
    path("event-venue-form", api.event_venue_form, name="event_venue_form"),

    path("entry-assign-form", api.entry_assign_form, name="entry_assign_form"),
    path("entry-confirm-form", api.entry_confirm_form, name="entry_confirm_form"),
    path("entry-reject-form", api.entry_reject_form, name="entry_reject_form"),

    path("manage-division-form/", api.manage_division_form, name="manage_division_form"),
    path("organization-division/", api.organization_division, name="organization_division"),
]
