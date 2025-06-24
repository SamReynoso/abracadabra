from models.models import (
    Event,
    Registration,
    Entry,
    Team,
    DivisionTeam,
)
from . import fragments
from models.helper import Helper
from .guests import with_owner, get_owner


class CoachHelper:
    class Get:
        @staticmethod
        def registration(data, owner):
            registration_slug = data.get('registration_slug', '')
            if not registration_slug:
                raise ValueError("Registration slug is required.")
            registration = Registration.from_slug(registration_slug)
            if not registration:
                raise ValueError("Registration not found.")
            if registration.owner != owner:
                raise ValueError("You do not have permission to access this registration.")
            return registration

        @staticmethod
        def registrations(owner):
            return Registration.objects.filter(owner=owner)

        @staticmethod
        def event(data):
            event_slug = data.get('event_slug', '')
            if not event_slug:
                raise ValueError("Event slug is required.")
            event = Event.from_slug(event_slug)
            if not event:
                raise ValueError("Event not found.")
            return event

        @staticmethod
        def entry(data, owner):
            entry_id = data.get('entry_id', '')
            if not entry_id:
                raise ValueError("Entry ID is required.")
            try:
                entry = Entry.objects.get(id=entry_id, registration__owner=owner)
            except Entry.DoesNotExist:
                raise ValueError("Entry not found.")
            return entry

        @staticmethod
        def team(data, owner):
            team_slug = data.get('team_slug', '')
            if not team_slug:
                raise ValueError("Team slug is required.")
            team = Team.from_slug(team_slug)
            if not team:
                raise ValueError("Team not found.")
            if team.owner != owner:
                raise ValueError("You do not have permission to access this team.")
            return team

        @staticmethod
        def division(data, owner):
            division_slug = data.get('division_slug', '')
            if not division_slug:
                raise ValueError("Division slug is required.")
            division = DivisionTeam.from_slug(division_slug)
            if not division:
                raise ValueError("Division not found.")
            if division.team.owner != owner:
                raise ValueError("You do not have permission to access this division.")
            return division


    class Create:
        @staticmethod
        def registration(data, owner):
            event = CoachHelper.Get.event(data)
            return Registration.objects.create(
                event=event,
                owner=owner,
                status=Registration.Status.DRAFT,
            )

        @staticmethod
        def team(data, owner):
            return Team.objects.create(
                name=data.get('name', 'Unnamed Team'),
                owner=owner,
            )

        @staticmethod
        def division(data, owner):
            team = CoachHelper.Get.team(data, owner)
            print("Creating division for team:", team.name)
            info = Helper.GetCreate.division(data)
            return DivisionTeam.objects.create(
                team=team,
                info=info,
            )

    class Update:
        @staticmethod
        def guest_contact_info(data, owner):
            guest = owner.guest
            guest.first_name = data.get('first_name', '')
            guest.last_name = data.get('last_name', '')
            guest.email = data.get('email', '')
            guest.phone = data.get('phone', '')
            guest.save()
            return owner

        @staticmethod
        def registration(data, owner):
            registration = CoachHelper.Get.registration(data, owner)
            return registration

        @staticmethod
        def team(data, owner):
            team = CoachHelper.Get.team(data, owner)
            team.name = data.get('name') 
            team.save()
            return team

        @staticmethod
        def division(data, owner):
            division = CoachHelper.Get.division(data, owner)
            info = Helper.GetCreate.division(data)
            division.info = info
            division.save()
            return division


@with_owner
def guest_contact_info_form(request):
    owner = get_owner(request)
    if request.method == 'POST':
        data = request.POST
        CoachHelper.Update.guest_contact_info(data, owner)
        return fragments.guest_contact_info(request, owner.guest)
    return fragments.guest_contact_info_form(request, owner.guest)


@with_owner
def handle_group_team_entry(request):
    division_ids = request.POST.getlist('divisions', [])
    registration_ids = request.POST.getlist('registration_ids', [])

    for reg_id in registration_ids:
        registration = Registration.objects.get(id=reg_id, owner=request.owner)
        at_least_one = False

        if request.POST.get(f'registration-{ reg_id }', '') == 'yes':
            for div_id in division_ids:
                key = f"{ reg_id }-{ div_id }"
                if request.POST.get(key, '') == 'yes':
                    division = DivisionTeam.objects.get(id=div_id)
                    Entry.objects.create(
                        registration=registration,
                        reported_division=division,
                        assigned_division=None,
                        status=Entry.Status.PENDING,
                    )
                    at_least_one = True
            if at_least_one:
                registration.status = Registration.Status.PENDING
                registration.save()


@with_owner
def event_registration_delete(request):
    owner = get_owner(request)
    if request.method == 'POST':
        data = request.POST
        registration = CoachHelper.Get.registration(data, owner)
        registration.delete()


@with_owner
def team_form(request):
    owner = get_owner(request)
    if request.method == 'POST':
        data = request.POST
        if "team_slug" in data:
            print("Updating team")
            team = CoachHelper.Update.team(data, owner)    
            return fragments.handle_team_update(request, team)
        else:
            print("Creating team")
            team = CoachHelper.Create.team(data, owner)
            return fragments.workspace_content(request, owner)

    data = request.GET
    if "team_slug" in data:
        team = CoachHelper.Get.team(data, owner)
        return fragments.team_form(request, team)
    raise ValueError("Invalid request data. 'team_slug' is required to update a team.")


@with_owner
def team_delete(request):
    owner = get_owner(request)
    if request.method == 'POST':
        data = request.POST
        team = CoachHelper.Get.team(data, owner)
        team.delete()
        return fragments.workspace_content(request, owner)
    data = request.GET
    if "team_slug" in data:
        team = CoachHelper.Get.team(data, owner)
        return fragments.team_delete_form(request, team)
    raise ValueError("Invalid request data. 'team_slug' is required to delete a team.")


@with_owner
def division_form(request):
    owner = get_owner(request)
    if request.method == 'POST':
        data = request.POST
        if "division_slug" in data:
            division = CoachHelper.Update.division(data, owner)
        else:
            division = CoachHelper.Create.division(data, owner)
        assert isinstance(division, DivisionTeam), "Division creation or update failed."
        return fragments.handle_division_update(request, division.team)
    data = request.GET
    if "team_slug" in data:
        team = CoachHelper.Get.team(data, owner)
        return fragments.division_form(request, team)
    raise ValueError("Invalid request data. 'division_slug' is required to update a division.")


@with_owner
def division_delete(request):
    owner = get_owner(request)
    if request.method == 'POST':
        data = request.POST
        division = CoachHelper.Get.division(data, owner)
        if division:
            team = division.team
            division.delete()
            return fragments.handle_division_update(request, team)
    raise ValueError("Invalid request method. POST is required to delete a division.")


@with_owner
def registration_form(request):
    owner = get_owner(request)
    if request.method == 'POST':
        data = request.POST
        if "registration_slug" in data:
            registration = CoachHelper.Update.registration(data, owner)
        else:
            registration = CoachHelper.Create.registration(data, owner)
        return fragments.workspace_content(request, owner)

    data = request.GET
    if "registration_slug" in data:
        registration = CoachHelper.Get.registration(data, owner)
        return fragments.registration_form(request, registration)
    raise ValueError("Invalid request data. 'event_slug' is required to create a registration.")


@with_owner
def registration_cancel_or_delete(request):
    owner = get_owner(request)
    if request.method == 'POST':
        data = request.POST
        registration = CoachHelper.Get.registration(data, owner)
        if registration.status == Registration.Status.DRAFT:
            registration.delete()
        elif registration.status == Registration.Status.CANCELLED:
            print("Registration reappling")
            registration.status = Registration.Status.PENDING
            registration.save()
        else:
            registration.status = Registration.Status.CANCELLED
            registration.save()
            entries = Entry.objects.filter(registration=registration)
            for entry in entries:
                entry.status = Entry.Status.CANCELLED
                entry.save()
        return fragments.workspace_content(request, owner)
    data = request.GET
    if "registration_slug" in data:
        registration = CoachHelper.Get.registration(data, owner)
        return fragments.registration_cancel(request, registration)
    raise ValueError("Invalid request data. 'registration_slug' is required to cancel a registration.")


@with_owner
def registration_submit(request):
    owner = get_owner(request)
    if request.method == 'POST':
        print("Submitting registration")
        data = request.POST
        registration = CoachHelper.Get.registration(data, owner)
        if registration.status != Registration.Status.DRAFT:
            raise ValueError("Only draft registrations can be submitted.")
        at_least_one = False
        for team in owner.teams.all():
            print(f"Processing team: {team.name}")
            for division in team.divisions.all():
                if request.POST.get(f"division{division.safe_slug}", '') == 'yes':
                    print(f"Creating entry for division: {division.info.name}")
                    Entry.objects.create(
                            team=team,
                            registration=registration,
                            reported_division=division.info,
                            assigned_division=None,
                            status=Entry.Status.PENDING,
                            )
                    at_least_one = True
        if at_least_one:
            registration.status = Registration.Status.PENDING
            registration.save()
        return fragments.registration_form(request, registration)
    raise ValueError("Invalid request method. Use POST to submit a registration.")


@with_owner
def entry_update(request):
    owner = get_owner(request)
    if request.method == 'POST':
        data = request.POST
        entry_ids = data.getlist('entry_ids', [])
        for entry_id in entry_ids:
            entry = CoachHelper.Get.entry({'entry_id': entry_id}, owner)
            action = data.get(f"entry_action_{ entry_id }", '')
            if action == "cancel":
                entry.status = Entry.Status.CANCELLED
                entry.save()
            if action == "register":
                if entry.status == Entry.Status.CANCELLED:
                    entry.status = Entry.Status.PENDING
                    entry.save()

        registration = CoachHelper.Get.registration(data, owner)
        return fragments.registration_form(request, registration)
    raise ValueError("Invalid request method. Use POST to update entries.")


