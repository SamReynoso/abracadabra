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

    path("new-event/", views.new_event_card, name="new_event_card"),
    path("event-card/<pk>/", views.event_card, name="event_card"),


    path("event-details/<safe_slug>/", views.event_details, name="event_details_fragment"),
    path("event-location/<safe_slug>/", views.event_location, name="event_location_fragment"),
    path("event-images/<safe_slug>/", views.event_images, name="event_images_fragment"),
    path("event-image-accept/<event_slug>/<image_slug>/", views.event_image_accept, name="event_image_accept_fragment"),
    path("event-form/<safe_slug>/", views.event_form, name="event_form_fragment"),

    path("event-lifecycle/<safe_slug>/", views.event_lifecycle, name="event_lifecycle_fragment"),
    path("event-manage/<safe_slug>/", views.event_manage, name="event_manage"),

    path("set-organization/<safe_slug>/", views.set_org, name="set_organization"),


    path("create-org-division/<safe_slug>/", views.create_org_division, name="create_org_division"),
    path("pending-confirmed/<safe_slug>/", views.pending_confirmed, name="pending_confirmed"),
    path("assign-entry/<safe_slug>/", views.assign_entry, name="assign_entry"),
    path("confirm-entry/<safe_slug>/", views.confirm_entry, name="confirm_entry"),
    path("reject-entry/<safe_slug>/", views.reject_entry, name="reject_entry"),
]
