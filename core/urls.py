from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("api/new-event/", views.new_event, name="api_new_event"),
]
