from django.urls import path
from . import views


urlpatterns = [
    path("", views.on_deck, name="app_on_deck"),
    path("images/", views.images, name="app_images"),
    path("memberships/", views.memberships, name="app_memberships"),
    path("following/", views.following, name="app_following"),
    path("orgs/", views.orgs, name="app_orgs"),
    path("teams/", views.teams, name="app_teams"),

    path("upload-image/", views.upload_image, name="upload_image"),
    path("update-image/<id>/", views.update_image, name="update_image"),

    path("image-details/<id>/", views.image_details, name="image_details"),
    path("day-card/", views.day_card, name="day_card"),
    path("event-form/", views.event_form, name="event_form"),
    path("new-event/", views.new_event_card, name="new_event_card"),
    path("event-card/<pk>", views.event_card, name="event_card"),
    path("event/<safe_slug>", views.event_manage, name="event_manage"),

    path("set-organization/<safe_slug>", views.set_org, name="set_organization"),
]
