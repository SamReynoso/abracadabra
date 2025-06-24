from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.on_deck, name="app_on_deck"),
    path("images/", views.images, name="app_images"),
    path("image-upload/", views.image_upload, name="image_upload"),
    path("image-form/", views.image_form, name="image_form"),
    path("image-delete/", views.image_delete, name="image_delete"),

    path("address-book/", views.address_book, name="app_address_book"),
    path("memberships/", views.memberships, name="app_memberships"),
    path("watch-list/", views.watch_list, name="app_watch_list"),
    path("teams/", views.teams, name="app_teams"),
    path("orgs/", views.orgs, name="app_orgs"),
    path("orgs/<safe_slug>/", views.select_org, name="select_org"),
    path("event-manage/<safe_slug>/", views.event_manage, name="event_manage"),
    path("event-details-fragment/", views.event_details_fragment, name="event_details_fragment"),
    path("event-delete/", views.event_delete, name="event_delete"),

    path("api/", include("app.api_urls"))
]
