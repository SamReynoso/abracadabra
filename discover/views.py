import uuid
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
import random

from models.models import (
        Event, 
        Guest,
        Organization,
        Membership,
        Owner,
        RegistrationEntry,
        TeamDivision, 
        User,
        EventType,
        EventStatus,
        RegistrationStatus,
        RegistrationEntryStatus,
        Registration,
        Role,
        Team
        )





def marketplace(request):
    return render(request, 'discover/marketplace.html')


def basketball(request):
    return render(request, 'discover/basketball.html')


def basketball_spotlight(request, page_number: str):
    page = int(page_number)
    events = Event.objects.all()
    print(f"Events for basketball spotlight: {events}")
    paginator = Paginator(events, 1)
    page_obj = paginator.get_page(page_number)
    context = {
        'events': page_obj,
        'next_page': page + 1 if int(page) < paginator.num_pages else None,
    }
    return render(request, 'discover/result_paginator.html', context)


def event_details(request, event_slug):
    event = Event.from_slug(event_slug)
    return render(request, 'discover/event-details.html', { 'event': event })

def clear_cookie(request):
    res = redirect(request, 'marketplace')
    guest_uuid = request.GET.get('guest_uuid', None) or request.COOKIES.get('guest_uuid', None)
    if guest_uuid:
        res.delete_cookie('guest_uuid')
        print(f"Cleared cookie for guest with UUID: {guest_uuid}")
    else:
        print("No guest UUID found in request, nothing to clear.")
    return res


def get_guest(request):
    guest_uuid = request.GET.get('guest_uuid', None) or request.COOKIES.get('guest_uuid', None)
    if guest_uuid:
        try:
            guest = Guest.objects.get(uuid=guest_uuid)
            print(f"Found guest with UUID: {guest_uuid}")
            return guest
        except Guest.DoesNotExist:
            print(f"Guest with UUID {guest_uuid} does not exist.")
            return None
    else:
        print("No guest UUID provided in request.")
        return None


def create_guest():
    guest = Guest.objects.create()
    Owner.objects.create(guest=guest)
    guest.save()
    return guest


def guest_logout_from_this_device(request):
    res = redirect('marketplace')
    if request.method == 'POST':
        guest = get_guest(request)
        if guest:
            res.delete_cookie('guest_uuid')
        return res
    return res


def guest_registration_helper(request, event):
    guest = get_guest(request)
    if guest is None:
        guest = create_guest()
    Registration.objects.create(event=event, owner=guest.owner)
    res = redirect('workspace')
    res.set_cookie('guest_uuid', guest.uuid, max_age=60*60*24*30)
    return res


def auth_registration_helper(request, event):
    return guest_registration_helper(request, event)


def event_register(request, safe_slug):
    if request.method == 'POST':
        event = Event.from_slug(safe_slug)
        if request.user.is_authenticated:
            print("User is authenticated, proceeding with auth registration flow for event:", event.name)
            return auth_registration_helper(request, event)
        else:
            print("Guest registration flow initiated for event:", event.name)
            return guest_registration_helper(request, event)
    return redirect('marketplace')


def contact_info(request):
    context = { 'guest': get_guest(request) }
    return render(request, 'discover/fragments/contact_info.html', context)



def contact_info_form(request):
    if request.method == 'POST':
        guest = get_guest(request)
        if guest is None:
            guest = create_guest()

        guest.first_name = request.POST.get('first_name', '')
        guest.last_name = request.POST.get('last_name', '')
        guest.email = request.POST.get('email', '')
        guest.phone = request.POST.get('phone', '')
        guest.save()
        context = { 'guest': guest }
        res = render(request, 'discover/fragments/contact_info.html', context)
        res.set_cookie('guest_uuid', guest.uuid, max_age=60*60*24*30)
        return res

    guest = get_guest(request)
    context = { 'guest': guest }
    return render(request, 'discover/fragments/contact_info_form.html', context)


def team_form(request):
    guest = get_guest(request)
    if request.method == 'POST' and guest:
        name = request.POST.get('name', '')
        Team.objects.create(name=name, owner=guest.owner)
    return render(request, 'discover/fragments/teams.html', {'guest': guest})


def division_form(request):
    guest = get_guest(request)
    if request.method == 'POST' and guest:
        team_id  = request.POST.get('team', '')
        team = Team.objects.filter(id=team_id, owner=guest.owner).first()
        if team:
            TeamDivision.objects.create(
                    team=team,
                    gender=request.POST.get('gender', ''),
                    age=request.POST.get('age', ''),
                    level=request.POST.get('level', ''),
                    )
    return redirect('teams')


def handle_teams_post(request):
    division_ids = request.POST.getlist('divisions', [])
    registration_ids = request.POST.getlist('registration_ids', [])
    for reg_id in registration_ids:
        registration = Registration.objects.get(id=reg_id)
        if request.POST.get(f'registration-{ reg_id }', '') == 'yes':
            at_least_one = False
            for div_id in division_ids:
                key = f"{ reg_id }-{ div_id }"
                if request.POST.get(key, '') == 'yes':
                    division = TeamDivision.objects.get(id=div_id)
                    RegistrationEntry.objects.create(
                        registration=registration,
                        reported_division=division,
                        assigned_division=None,
                        status=RegistrationEntryStatus.PENDING,
                    )
                    print(f"Created registration entry for registration {reg_id} and division {div_id}")
                    at_least_one = True
            if at_least_one:
                registration.status = RegistrationStatus.PENDING
                registration.save()


def teams(request):
    if request.method == 'POST':
        handle_teams_post(request)

    guest = get_guest(request)
    context = {
        'guest': guest,
        'teams': Team.objects.filter(owner=guest.owner),
        'registrations': Registration.objects.filter(owner=guest.owner),
    }
    return render(request, 'discover/fragments/teams.html', context)


def workspace(request):
    guest = get_guest(request)
    if guest is None:
        print("No guest found, creating a new guest.")
        guest = create_guest()
        print("New guest created with UUID:", guest.uuid)
    
    context = {
        'guest': guest,
        'registrations': Registration.objects.filter(owner=guest.owner),
        'teams': Team.objects.filter(owner=guest.owner),
    }
    return render(request, 'discover/workspace.html', context)


def org_details(request, org_slug):
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

