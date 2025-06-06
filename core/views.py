from django.shortcuts import render, redirect
from models.models import Event, Membership, Role
from app.forms import EventForm




def director_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        membership = Membership.objects.filter(user=request.user, role=Role.DIRECTOR).first()
        if membership:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('app_orgs')
    return _wrapped_view



def home(request):
    return render(request, "core/home.html")


@director_required
def new_event(request):
    primary_org = request.user.memberships.filter(role=Role.DIRECTOR, primary=True).first()
    assert primary_org, "User must have a primary organization with director role"
    default_data = {
        "organization": primary_org.organization.id,
        "name": "New Event",
        "event_type": "Conference",
        "organization": primary_org.organization,
    }
    event = Event.objects.create(**default_data)
    event.save()
    context = {
        "event": event,
        "card_id": event.pk,
    }
    return render(request, "app/fragments/event_card.html", context)
