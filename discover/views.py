from django.shortcuts import render, redirect

from models.models import (
        Event, 
        Organization,
        User,
        Sports,
        Team,
        Registration,
        )

from . import fragments
from .api import CoachHelper
from .guests import with_owner, get_owner



def marketplace(request):
    return render(request, 'discover/marketplace.html')


def basketball(request):
    context = { 'sport': Sports.BASKETBALL }
    return render(request, 'discover/basketball.html', context)


def event_details(request, event_slug):
    event = Event.from_slug(event_slug)
    return render(request, 'discover/event_details.html', { 'event': event })


@with_owner
def event_registration(request):
    owner = get_owner(request)
    if request.method == 'POST':
        data = request.POST
        if "registration_slug" in data:
            CoachHelper.Update.registration(data, owner)
        else:
            print("Creating new registration")
            CoachHelper.Create.registration(data, owner)
        return redirect('workspace')
    raise ValueError("Invalid request method. Use POST to create or update a registration.")


@with_owner
def workspace(request):
    owner = get_owner(request)
    context = { 'owner': owner }
    return render(request, 'discover/workspace.html', context)

@with_owner
def workspace_content(request):
    owner = get_owner(request)
    context = { 
               'teams': Team.objects.filter(owner=owner),
               'registrations': Registration.objects.filter(owner=owner),
               }
    return render(request, 'discover/fragments/workspace_content.html', context)


@with_owner
def registration_details(request):
    owner = get_owner(request)
    data = request.GET
    registration = CoachHelper.Get.registration(data, owner)

    context = { 'registration': registration }
    return render(request, 'discover/fragments/registration_details.html', context)


@with_owner
def contact_info(request):
    owner = get_owner(request)
    return fragments.guest_contact_info(request, owner.guest)


def organization_details(request, org_slug):
    context = { "organization": Organization.from_slug(org_slug) }
    return render(request, 'discover/organization_details.html', context)


def user_persona(request, user_slug):
   user = User.from_slug(user_slug)
   context = { 'persona': user }
   return render(request, 'discover/user_persona.html', context)
