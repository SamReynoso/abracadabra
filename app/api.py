from models.models import (
        DivisionOrg,
        Venue,
        DivisionOrg,
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



def event_poster_accept(request):
    user = request.user
    if request.method != "POST":
        event = Helper.Get.event(request.POST, user)
        event.poster = image
        event.save()


def event(request):
    user = request.user
    if request.method == "POST":
        data = request.POST
        if 'event_slug' not in data:
            Helper.Create.event(data, user)
        Helper.Update.event(data, user)


def create_org_division(request):
    if request.method == "POST":
        user = request.user
        data = request.POST
        Helper.Create.organization_division(data, user)


def event_delete(request):
    if request.method == "POST":
        event =  Helper.Get.event(request.POST, request.user)
        event.delete()


def event_venue(request):
    if request.method == "POST":
        data = request.POST
        event = Helper.Get.event(data, request.user)
        if 'address' in data:
            address  = Helper.Get.address(data, request.user)
        else:
            address = Helper.Create.address(data, request.user)
        Handle.venue_create(event, address)


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


def image(request):
    user = request.user
    if request.method == "POST":
        data = request.POST
        if 'image_slug' in data:
            Helper.Update.image(data, user)
        else:
            Helper.Create.image(data, user)
