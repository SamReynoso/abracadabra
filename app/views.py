from django.shortcuts import render
from django.http import HttpResponse
import random


def index(request):
    jwt = request.COOKIES.get("jwt")
    print("[APP app] : jwt ------->", jwt)
    print("this is the app", "-" * 20)
    user = request.user
    if user.is_authenticated:
        print("User is authenticated:", user.username)
    else:
        print("User is not authenticated", user)
    return render(request, "core/index.html")


COUNT = 0
def day_card(request):
    play_areas = [
            { "label": "Play Area 1", "id": 1 },
            { "label": "Play Area 2", "id": 2 },
            { "label": "Play Area 3", "id": 3 },
            { "label": "Play Area 4", "id": 4 },
            { "label": "Play Area 5", "id": 5 },
            { "label": "Play Area 6", "id": 6 },
            { "label": "Play Area 7", "id": 7 },
            { "label": "Play Area 8", "id": 8 },
            { "label": "Play Area 9", "id": 9 },
            { "label": "Play Area 10", "id": 10 },
            { "label": "Play Area 11", "id": 11 },
            { "label": "Play Area 12", "id": 12 },
            { "label": "Play Area 13", "id": 13 },
            { "label": "Play Area 14", "id": 14 },
            { "label": "Play Area 15", "id": 15 },
            { "label": "Play Area 16", "id": 16 },
            { "label": "Play Area 17", "id": 17 },
            { "label": "Play Area 18", "id": 18 },
            { "label": "Play Area 19", "id": 19 },
            { "label": "Play Area 20", "id": 20 },
            ]

    time_slots = [
            { "label": "5:00 AM", "id": 1 },
            { "label": "6:00 AM", "id": 1 },
            { "label": "7:00 AM", "id": 1 },
            { "label": "8:00 AM", "id": 1 },
            { "label": "9:00 AM", "id": 1 },
            { "label": "10:00 AM", "id": 2 },
            { "label": "11:00 AM", "id": 3 },
            { "label": "12:00 PM", "id": 4 },
            { "label": "1:00 PM", "id": 5 },
            { "label": "2:00 PM", "id": 6 },
            { "label": "3:00 PM", "id": 7 },
            { "label": "4:00 PM", "id": 8 },
            { "label": "5:00 PM", "id": 9 },
            { "label": "6:00 PM", "id": 10 },
            { "label": "7:00 PM", "id": 11 },
            { "label": "8:00 PM", "id": 12 },
            { "label": "9:00 PM", "id": 13 },
            { "label": "10:00 PM", "id": 14 },
            { "label": "11:00 PM", "id": 15 },
            { "label": "12:00 AM", "id": 16 },
            { "label": "1:00 AM", "id": 17 },
            { "label": "2:00 AM", "id": 18 },
            { "label": "3:00 AM", "id": 19 },
            { "label": "4:00 AM", "id": 20 },
        ]

    global COUNT
    if COUNT == 0:
        context = {
            "day_number": random.randint(1, 100),
            "label": "Auto-generated Day",
            "play_areas": play_areas,
            "time_slots": time_slots,
        }
        COUNT += 1
    else:
        context = {
            "day_number": COUNT,
            "label": f"Day {COUNT}",
            "play_areas": play_areas[:5],
            "time_slots": time_slots[:5],
        }
        COUNT += 1
    return render(request, "core/day_card.html", context)
