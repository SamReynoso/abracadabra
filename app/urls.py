from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="home"),
    path("app/day-card/", views.day_card, name="day_card"),
]
