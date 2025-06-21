from django.shortcuts import render
from models.models import Sports, Event, Team, Venue, Game


def search(request):
    page = request.GET.get('page', 1)
    sport = request.GET.get('sport')
    events = Event.objects.filter(sport=sport).order_by('-created_at')

    context = {
        'page': int(page) + 1,
        'events': events,
        'sport': sport,
    }
    if page == '1':
        print("Rendering spotlight results with events:", events)
        return render(request, 'search/results_spotlight.html', context)
    print("Rendering wide results")
    return render(request, 'search/results_wide.html', context)
