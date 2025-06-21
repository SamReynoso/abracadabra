from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.on_deck, name="app_on_deck"),
    path("images/", views.images, name="app_images"),
    path("address-book/", views.address_book, name="app_address_book"),
    path("memberships/", views.memberships, name="app_memberships"),
    path("watch-list/", views.watch_list, name="app_watch_list"),
    path("teams/", views.teams, name="app_teams"),
    path("orgs/", views.orgs, name="app_orgs"),
    path("orgs/<safe_slug>/", views.select_org, name="select_org"),
    path("event-manage/<safe_slug>/", views.event_manage, name="event_manage"),

    path("api/", include("app.api_urls"))
]
