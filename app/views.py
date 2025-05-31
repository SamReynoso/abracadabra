from django.shortcuts import render
import random
from models.models import Event, Organization, Membership, Role
from .forms import EventForm, NewOrganizationForm


def director(request):
    memberships =  Membership.objects.filter(user=request.user, role=Role.DIRECTOR)
    organizations = []
    organization = None

    if memberships.exists():
        organizations = [membership.organization for membership in memberships]
        primary_membership = memberships.filter(primary=True).first()
        assert primary_membership is not None, "Primary membership should exist"
        organization = primary_membership.organization 
    context = {
            'organization': organization, 
            'organizations': organizations,
            }

    if request.method == "POST":
        form = NewOrganizationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            organization = Organization.objects.create(name=data['name'])
            organization.save()
            organization.set_primary()
            membership = Membership.objects.create(
                user=request.user,
                organization=organization,
                role=Role.DIRECTOR
            )
            membership.save()
            membership.set_primary()
            context['organization'] = organization
            context['organizations'].append(organization)
        else:
            context['form'] = form
            context['errors'] = form.errors
    else:
        context['form'] = NewOrganizationForm()

    return render(request, "app/director.html", context)


COUNT = 0
def event_form(request):
    global COUNT
    context = {
        "id": COUNT,
    }
    return render(request, "app/event_fragment.html", context)


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
    return render(request, "app/day_card.html", context)
