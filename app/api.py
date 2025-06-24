from app.forms import EventForm
from models.models import (
        DivisionOrg,
        Venue,
        DivisionOrg,
        Entry,
        )
from models.helper import Helper
from . import fragments



class Handle:
        @staticmethod
        def venue_create(event, address):
            venue, _ = Venue.objects.get_or_create(
                event=event,
                address=address,
            )
            return venue


class DirectorHelper:
    class Get:
        @staticmethod
        def entry(data, user):
            entry_slug = data.get('entry_slug', '')
            if not entry_slug:
                raise ValueError("Entry slug is required.")
            try:
                entry = Entry.from_slug(entry_slug)
            except Entry.DoesNotExist:
                raise ValueError("Entry not found.")
            if entry.registration.event.organization.director != user:
                raise ValueError("You do not have permission to access this entry.")
            return entry



def event_form(request):
    user = request.user
    if request.method == "POST":
        data = request.POST
        if 'event_slug' not in data:
            event = Helper.Create.event(data, user)
            return fragments.event_card(request, event)
        else:
            event = Helper.Get.event(data, user)
            form = EventForm(instance=event, data=data)
            if form.is_valid():
                form.save()
                return fragments.event_card(request, event)

            return fragments.event_form(request, event, form)

    data = request.GET
    event = Helper.Get.event(data, user)
    form = EventForm(instance=event)
    return fragments.event_form(request, event, form)


def event_poster_select(request):
    user = request.user
    if request.method == "POST":
        data = request.POST
        event = Helper.Get.event(data, user)
        image = Helper.Get.image(data, user)
        return fragments.event_poster_accept(request, event, image)
    data = request.GET
    event = Helper.Get.event(data, user)
    images = Helper.Get.images(user)
    return  fragments.event_poster_select(request, event, images)


def event_poster_accept(request):
    user = request.user
    if request.method == "POST":
        data = request.POST
        event = Helper.Get.event(data, user)
        image = Helper.Get.image(data, user)
        event.poster = image
        event.save()
        return fragments.event_details(request, event)

    data = request.GET
    event = Helper.Get.event(data, user)
    image = Helper.Get.image(data, user)
    return fragments.event_poster_accept(request, event, image)


def event_venue_form(request):
    user = request.user
    if request.method == "POST":
        data = request.POST
        event = Helper.Get.event(data, user)
        if 'address' in data:
            address  = Helper.Get.address(data, request.user)
        else:
            address = Helper.Create.address(data, request.user)
        Handle.venue_create(event, address)
        return fragments.event_venue_form(request, event)
    data = request.GET
    event = Helper.Get.event(data, user)
    return fragments.event_venue_form(request, event)


def event_delete(request):
    if request.method == "POST":
        event =  Helper.Get.event(request.POST, request.user)
        event.delete()



def entry_assign_form(request):
    user = request.user
    if request.method == "POST":
        data = request.POST
        entry = DirectorHelper.Get.entry(data, user)
        return fragments.entry_card(request, entry)
    data = request.GET
    entry = DirectorHelper.Get.entry(data, user)
    return fragments.entry_assign_form(request, entry)



def entry_confirm_form(request):
    user = request.user
    if request.method == "POST":
        data = request.POST
        entry = DirectorHelper.Get.entry(data, user)
        entry.status = Entry.Status.CONFIRMED
        entry.save()
        return fragments.entry_details(request, entry)
    data = request.GET
    entry = DirectorHelper.Get.entry(data, user)
    return fragments.entry_confirm_form(request, entry)


def entry_reject_form(request):
    user = request.user
    if request.method == "POST":
        data = request.POST
        entry = DirectorHelper.Get.entry(data, user)
        entry.status = Entry.Status.REJECTED
        entry.save()
        return fragments.entry_details(request, entry)
    data = request.GET
    entry = DirectorHelper.Get.entry(data, user)
    return fragments.entry_reject_form(request, entry)


def create_org_division(request):
    if request.method == "POST":
        user = request.user
        data = request.POST
        Helper.Create.organization_division(data, user)


def manage_division_form(request):
    user = request.user
    data = request.GET
    event = Helper.Get.event(data, user)
    return fragments.manage_division_form(request, event)

def organization_division(request):
    user = request.user
    if request.method == "POST":
        data = request.POST
        organization = Helper.Get.organization(data, user)
        if 'division_org_id' not in data:
            division_info = Helper.GetCreate.division(request.POST)
            DivisionOrg.objects.create(
                organization=organization,
                division_info=division_info
            )
        else:
            division_org = DivisionOrg.objects.get(
                id=data.get('division_org_id'),
                organization=organization
            )
            division_info = Helper.GetCreate.division(request.POST)
            division_org.info = division_info
            division_org.save()


