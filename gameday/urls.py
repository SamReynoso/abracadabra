from django.urls import path
from . import views


urlpatterns = [
    path("", views.gameday, name="gameday"),
    path("division/", views.division, name="gameday_division"),
    path("game/", views.game, name="gameday_game"),
    path("scoreboard/", views.scoreboard, name="gameday_scoreboard"),
]
