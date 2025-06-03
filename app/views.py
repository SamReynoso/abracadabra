from django.shortcuts import redirect, render
import random
from models.models import (
        Event,
        Organization,
        Membership,
        Role,
        EventType,
        EventStatus,
        Images,

        )
from .forms import EventForm, NewOrganizationForm


def set_profile_picture(request, context):
    profile_picture = Images.objects.filter(
        user=request.user, is_profile_picture=True
    ).first()
    if profile_picture:
        profile_picture_url = profile_picture.image.url
    else:
        profile_picture_url = None
    context['profile_picture_url'] = profile_picture_url

def on_deck(request):
    context = {
        'user': request.user,
    }
    set_profile_picture(request, context)
    return render(request, "app/on-deck.html", context)


def images(request):
    images = Images.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'images': images,
    }
    set_profile_picture(request, context)
    return render(request, "app/images.html", context)


def image_details(request, id):
    try:
        image = Images.objects.get(id=id, user=request.user)
    except Images.DoesNotExist:
        return render(request, "app/image_not_found.html", {"image_id": id})

    context = {
        'image': image,
    }
    set_profile_picture(request, context)
    return render(request, "app/fragments/image_details.html", context)


def update_image(request, id):
    try:
        image = Images.objects.get(id=id, user=request.user)
    except Images.DoesNotExist:
        raise ValueError("Image not found or you do not have permission to update it.")
    if request.method == "POST":
        caption = request.POST.get('caption', '')
        is_profile_picture = request.POST.get('is_profile_picture', 'off') == 'on'
        print(f'''


              {is_profile_picture}


              ''')
        if is_profile_picture:
            Images.objects.filter(user=request.user, is_profile_picture=True).update(is_profile_picture=False)
        image.is_profile_picture = is_profile_picture
        image.caption = caption
        image.save()
    images = Images.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'images': images,
    }
    set_profile_picture(request, context)
    return render(request, "app/images.html", context)

def upload_image(request):
    if request.method == "POST":
        image = request.FILES.get('image')
        if image:
            img = Images.objects.create(
                    image=image,
                    user=request.user,
                    caption=request.POST.get('caption', ''),
                    )
            img.save()
            return render(request, "app/imgages.html", {"image": img})
        else:
            return render(request, "app/upload_error.html", {"error": "No image provided."})
    return render(request, "app/upload_image.html", {})

def memberships(request):
    context = {}
    set_profile_picture(request, context)
    return render(request, "app/memberships.html", context)

def following(request):
    context = {}
    set_profile_picture(request, context)
    return render(request, "app/following.html", context)


def teams(request):
    memberships = Membership.objects.filter(user=request.user, role=Role.DIRECTOR)
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

    set_profile_picture(request, context)
    return render(request, "app/teams.html", context)


def set_org(request, safe_slug: str):
    organization = Organization.from_slug(safe_slug)
    membership = Membership.objects.filter(organization=organization, user=request.user).first()
    if membership is None:
        return render(request, "app/org_not_found.html", {"safe_slug": safe_slug})
    membership.set_primary()
    return redirect('app_orgs')


def orgs(request):
    memberships =  Membership.objects.filter(user=request.user, role=Role.DIRECTOR)
    organizations = []
    organization = None

    if memberships.exists():
        organizations = [membership.organization for membership in memberships]
        primary= memberships.filter(primary=True)
        print(primary)
        primary_membership = primary.first() if primary.exists() else None
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

    set_profile_picture(request, context)
    return render(request, "app/orgs.html", context)



def event_manage(request, safe_slug: str | None):
    if safe_slug is None:
        return render(request, "app/event_not_found.html", {"safe_slug": safe_slug})
    try:
        event = Event.from_slug(safe_slug)
    except Event.DoesNotExist:
        return render(request, "app/event_not_found.html", {"safe_slug": safe_slug})

    context = {
        'event': event,
    }
    return render(request, "app/event_details.html", context)


def event_card(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return render(request, "app/event_not_found.html", {"pk": pk})

    context = {
        'event': event,
        'card_id': event.pk,
    }
    return render(request, "app/event_card.html", context)


def new_event_card(request):
    user = request.user
    org = user.memberships.filter(role=Role.DIRECTOR, primary=True).first()
    card_id = "newEvent"
    event = Event.objects.create(
        organization=org.organization if org else None,
        name="New Event",
        status=EventStatus.CREATED,
    )
    context = {
        'card_id': card_id,
        'event': event,
    }
    return render(request, "app/event_card.html", context)



def event_form(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.save()
            context = {
                "event": event,
                "card_id": event.pk,
            }
            return render(request, "app/event_card.html", context)
        else:
            context = {
                "form": form,
                "card_id": "newEvent",
            }
    else:
        form = EventForm()
        context = {
            "card_id": "newEvent",
            "form": form,
        }
    return render(request, "app/event_form.html", context)



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



