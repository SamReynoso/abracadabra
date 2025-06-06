import time
from django.shortcuts import redirect, render
from models.models import (
        Address,
        Event,
        Location,
        Organization,
        Membership,
        Role,
        EventType,
        EventStatus,
        Images,

        )
from .forms import EventForm, LifeCycleForm, NewOrganizationForm


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
    organization = None
    organizations = Organization.objects.none()
    events = Event.objects.none()  # Default to empty queryset if no memberships

    if memberships.exists():
        organizations = [membership.organization for membership in memberships]
        primary= memberships.filter(primary=True)
        print(primary)
        primary_membership = primary.first() if primary.exists() else None
        assert primary_membership is not None, "Primary membership should exist"
        organization = primary_membership.organization 
        events = organization.events.all().order_by('-created_at')

    context = {
            'organization': organization, 
            'organizations': organizations,
            'in_progress': events.filter(status=EventStatus.CREATED),
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



def new_event_card(request):
    user = request.user
    org = user.memberships.filter(role=Role.DIRECTOR, primary=True).first()
    assert org is not None, "User must have a primary organization with director role"
    event = Event.objects.create(
        organization=org.organization,
        name="New Event",
        status=EventStatus.CREATED,
    )
    context = {
        'event': event,
    }
    return render(request, "app/fragments/event_card.html", context)


def event_card(request, safe_slug: str):
    context = { 'event': Event.from_slug(safe_slug) }
    return render(request, "app/fragments/event_card.html", context)


def event_details(request, safe_slug: str):
    context = { 'event': Event.from_slug(safe_slug) }
    return render(request, "app/fragments/event_details.html", context)


def event_location(request, safe_slug: str):
    event = Event.from_slug(safe_slug)
    assert event is not None, "Event must exist for the given slug"
    if request.method == "POST":
        address_id = request.POST.get('address', '')
        if address_id:
            address  = Address.objects.get(id=address_id, user=request.user)
            location = Location.objects.create(
                event=event,
                address=address,
            )
            location.save()
        else:
            print("Creating new address for event location")
            address = Address.objects.create(
                user=request.user,
                name=request.POST.get('name', ''),
                street=request.POST.get('street', ''),
                city=request.POST.get('city', ''),
                state=request.POST.get('state', ''),
                postal_code=request.POST.get('postal_code', ''),
            )
            address.save()
            location = Location.objects.create(
                event=event,
                address=address,
            )
            location.save()

    addresses = Address.objects.filter(user=request.user).order_by('-created_at')
    context = {
            "event": event,
            "addresses": addresses,
            }
    return render(request, "app/fragments/event_location.html", context)


def event_image_accept(request, event_slug: str, image_slug: str):
    event = Event.from_slug(event_slug)
    image = Images.from_slug(image_slug)
    assert event is not None, "Event must exist for the given slug"
    assert image is not None, "Image must exist for the given slug"

    if request.method == "POST":
            event.poster = image
            event.save()
            return render(
                    request,
                    "app/fragments/event_details.html",
                    {
                        "event": event
                        }
                    )

    context = {
            "event": event,
            "image": image,
            }
    return render(request, "app/fragments/event_image_accept.html", context)


def event_images(request, safe_slug: str):
    images = list(Images.objects.filter(user=request.user).order_by('-created_at'))

    context = {
            "event": Event.from_slug(safe_slug),
            "images": images * 5,  # For demonstration, repeat images to fill space
            }
    return render(request, "app/fragments/event_images.html", context)

def event_form(request, safe_slug: str):
    event = Event.from_slug(safe_slug)
    assert event is not None, "Event must exist for the given slug"
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        print("Form data:", request.POST)
        if form.is_valid():
            form.save()
            context = { "event": event }
            return render(request, "app/fragments/event_details.html", context)
        else:
            print("form errors:", form.errors)
            context = { "event": event, "form": form, }
    else:
        form = EventForm(instance=event)
        context = {
            "event": event,
            "form": form,
        }
    return render(request, "app/fragments/event_form.html", context)


def event_lifecycle(request, safe_slug: str):
    event = Event.from_slug(safe_slug)
    assert event is not None, "Event must exist for the given slug"
    if request.method == "POST":
        form = LifeCycleForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            context = { "event": event }
    else:
        form = LifeCycleForm(instance=event)
    context = {
        "event": event,
        "form": form,
    }
    return render(request, "app/fragments/event_lifecycle.html", context)




