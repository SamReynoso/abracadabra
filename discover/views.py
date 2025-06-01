from django.shortcuts import render
import random

from models.models import Event, Organization, Membership, User, EventType, EventStatus, RegistrationStatus, Registration, Role


def marketplace(request):
    return render(request, 'discover/marketplace.html')

def basketball(request):
    return render(request, 'discover/basketball.html')


def event_details(request, event_slug):
    event = Event.from_slug(event_slug)
    return render(request, 'discover/event-details.html')


def event_register(request):
    return render(request, 'discover/event-register.html')


def org_details(request, org_slug):
    print(f'''


          {org_slug}



          ''')
    org = Organization.from_slug(org_slug)
    assert org, "Organization not found"
    memberships = org.memberships.all()
    print(f"Memberships for org {org.name}: {memberships}")
    director = memberships.filter(role=Role.DIRECTOR).first()
    print(f"Director for org {org.name}: {director}")
    context = {
        'organization': org,
        'memberships': memberships,
        'director': director,
        'events': org.events.all(),
    }
    return render(request, 'discover/org-details.html', context)


def dashboard(request):
    return render(request, 'discover/dashboard.html')


def persona(request, user_slug):
   user = User.from_slug(user_slug)
   context = {
           'persona': user,
           }
   return render(request, 'discover/persona-details.html', context)


PAGES = list(range(100, 2000))
def load_more(request):
    global PAGES
    context = {
            'next_page': PAGES.pop() if PAGES else None,
            'events': [ 
                       {
                           'id': random.randint(1000, 9999),
                           'title': 'EVENT Tournament',
                            'date': 'DATE 2023-10-15',
                            'short_description': 'SHORT DIS Join us for an\
                                    exciting basketball tournament featuring\
                                    top teams from the region.',
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

