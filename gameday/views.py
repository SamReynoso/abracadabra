from django.shortcuts import render


def gameday(request):
    return render(request, "gameday/gameday.html")

def division(request):
    return render(request, "gameday/division.html")

def game(request):
    return render(request, "gameday/game.html")    

def scoreboard(request):
    return render(request, "gameday/scoreboard.html")    
