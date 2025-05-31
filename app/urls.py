from django.urls import path
from . import views


urlpatterns = [
    path("", views.director, name="director"),
    path("day-card/", views.day_card, name="day_card"),
    path("event-form/", views.event_form, name="event_form"),
]
