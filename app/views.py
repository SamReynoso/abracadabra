from django.shortcuts import redirect, render
from models.models import (
        Organization,
        Membership,
        Event,
        Address,
        )
from .forms import NewOrganizationForm
from models.helper import Helper
from . import fragments



def on_deck(request):
    context = {
        'user': request.user,
        # TODO: Add logic to fetch new registrations, and entry updates ;
    }
    return render(request, "app/on-deck.html", context)


def images(request):
    context = { 'images': request.user.images.all().order_by('-created_at') }
    return render(request, "app/images.html", context)


def image_upload(request):
    user = request.user
    if request.method == "POST":
        data = request.POST
        files = request.FILES
        Helper.Create.image(data, files, user)
        return redirect('app_images')
    raise ValueError("Invalid request method. Only POST is allowed.")


def image_form(request):
    user = request.user
    if request.method == "POST":
        data = request.POST
        image = Helper.Update.image(data, user)
        return redirect('app_images')
    else:
        data = request.GET 
        image = Helper.Get.image(data, user)
    return fragments.image_form(request, image)



def image_delete(request):
    user = request.user
    if request.method == "POST":
        data = request.POST
        image = Helper.Get.image(data, user)
        image.delete()
        return redirect('app_images')
    raise ValueError("Invalid request method. Only POST is allowed.")


def address_book(request):
    context = {
            "addresses": Address.objects.filter(user=request.user).order_by('-created_at'),
    }
    return render(request, "app/address_book.html", context)


def memberships(request):
    context = {
        'memberships': Membership.objects.filter(user=request.user).order_by('-created_at'),
    }
    return render(request, "app/memberships.html", context)


def watch_list(request):
    # This is not needed for the MVP, # but could be used to track events the user is interested in.
    context = {}
    return render(request, "app/following.html", context)


def teams(request):
    # This needs to be implemented, but for now we can just return an empty context.
    context = { }
    return render(request, "app/teams.html", context)



def orgs(request):
    directorships =  Membership.objects.filter(user=request.user, role=Membership.Role.DIRECTOR)

    if directorships.exists():
        prime = directorships.filter(selected=True).first()

        context = {
                'form': NewOrganizationForm(),
                'organizations': [membership.organization for membership in directorships],
                'organization': prime.organization if prime else None,
                'events': prime.organization.events.all().order_by('-created_at') if prime else [],
                'members': prime.organization.memberships.all().order_by('-created_at') if prime else [],
                }
    else:
        context = {
            'form': NewOrganizationForm(),
            'organizations': [],
            'organization': None,
            'events': [],
            'members': [],
        }

    if request.method == "POST":
        form = NewOrganizationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            organization = Organization.objects.create(
                    name=data['name'],
                    director=request.user,
                    )
            organization.save()
            Membership.objects.create(
                user=request.user,
                organization=organization,
                role=Membership.Role.DIRECTOR
            ).select()
            context['organization'] = organization
            context['organizations'].append(organization)
        else:
            context['form'] = form
            context['errors'] = form.errors

    return render(request, "app/orgs.html", context)


def select_org(request):
    if request.method == "POST":
        org_slug = request.POST.get('org_slug', '')
        organization = Organization.from_slug(org_slug)
        membership = Membership.objects.filter(
                organization=organization,
                user=request.user
                ).first()
        if membership:
            membership.select()
    return redirect('app_orgs')


def event_details_fragment(request):
    event = Helper.Get.event(request.GET, request.user)
    return fragments.event_details(request, event)


def event_delete(request):
    user = request.user
    if request.method == "POST":
        data = request.POST
        event = Helper.Get.event(data, request.user)
        event.delete()
        return redirect('app_orgs')
    data = request.GET
    event = Helper.Get.event(data, user)
    return fragments.event_delete_form(request, event)


def event_manage(request, safe_slug: str):
    event = Event.from_slug(safe_slug)
    context = { "event": event, }
    return render(request, "app/event_manage.html", context)


