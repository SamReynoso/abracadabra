from django.shortcuts import render
import random


def marketplace(request):
    return render(request, 'discover/marketplace.html')

def basketball(request):
    return render(request, 'discover/basketball.html')

def event_details(request):
    return render(request, 'discover/event-details.html')

def event_register(request):
    return render(request, 'discover/event-register.html')

def org(request):
    return render(request, 'discover/org-details.html')

def dashboard(request):
    return render(request, 'discover/dashboard.html')

def persona(request):
    return render(request, 'discover/persona-details.html')


PAGES = list(range(100, 2000))

def load_more(request):
    global PAGES
    print("Loading more events <---------------------")
    print("PAGES:", PAGES)
    context = {
            'next_page': PAGES.pop() if PAGES else None,
            'events': [ 
                       {
                           'title': 'EVENT Tournament',
                            'date': 'DATE 2023-10-15',
                            'short_description': 'SHORT DIS Join us for an exciting basketball tournament featuring top teams from the region.',
                            'poster_url': f"/mock-poster/{ random.randint(1000, 9999) }",
                            'org': {
                                'name': 'ORG Association',
                            }
                        },
                       ]
            }
    res = render(request, 'core/fragments/event-results.html', context)    
    res["Cache-Control"] = "no-cache, no-store, must-revalidate"
    res["Pragma"] = "no-cache"
    res["Expires"] = "0"
    return res

