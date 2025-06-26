import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models, transaction


class Sports(models.TextChoices):
    BASKETBALL = 'basketball', 'Basketball'


class ABSClass(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    @property
    def safe_slug(self) -> str:
        if self.pk is None:
            return "not-found"
        return str(self.pk)

    @classmethod
    def from_slug(cls,  slug: str):
        pk = str(slug)
        try:
            return cls.objects.get(pk=pk)
        except cls.DoesNotExist:
            raise ValueError(f"{cls.__name__} with slug '{slug}' does not exist.")

    class Meta:
        abstract = True


class Images(ABSClass):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_images/')
    caption = models.CharField(max_length=255, blank=True)
    is_profile_picture = models.BooleanField(default=False)

    @property
    def display_name(self):
        return "foobar"


class User(AbstractUser):
    profile_picture = models.ForeignKey(
            Images,
            related_name='profile_pictures',
            on_delete=models.SET_NULL,
            blank=True,
            null=True
            )

    @property
    def safe_slug(self) -> str:
        return f"{self.first_name}-{self.last_name}-{self.pk}"

    @classmethod
    def from_slug(cls,  slug: str):
        pk = slug.split('-')[-1]
        try:
            return cls.objects.get(pk=pk)
        except cls.DoesNotExist:
            raise ValueError(f"User with slug '{slug}' does not exist.")

    @property
    def profile_picture_url(self):
        if self.profile_picture:
            return self.profile_picture.url
        return "/assets/defaults/anonymous-user.svg"

    @property
    def display_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username


class Guest(ABSClass):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4)


class Contanct(ABSClass):
    contact_of = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            related_name='contacts',
            on_delete=models.CASCADE,
            blank=True,
            null=True
            )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)


class Owner(ABSClass):
    auth_user = models.OneToOneField(
            settings.AUTH_USER_MODEL,
            related_name='owner',
            on_delete=models.DO_NOTHING,
            default=None,
            blank=True,
            null=True
            )
    guest = models.OneToOneField(
            Guest,
            related_name='owner',
            on_delete=models.DO_NOTHING,
            default=None,
            blank=True,
            null=True
            )
    contact = models.OneToOneField(
            Contanct,
            related_name='owner',
            on_delete=models.DO_NOTHING,
            default=None,
            blank=True,
            null=True
            )

    @property
    def is_authenticated(self) -> bool:
        return self.auth_user is not None

    @property
    def info(self):
        if self.auth_user:
            return self.auth_user
        elif self.guest:
            return self.guest
        elif self.contact:
            return self.contact
        raise ValueError("Owner must have either an auth_user, guest, or contact associated.")

    def save(self, *args, **kwargs):
        if not self.auth_user and not self.guest and not self.contact:
            raise ValueError("Owner must have either an auth_user, guest, or contact associated.")
        super().save(*args, **kwargs)


class Organization(ABSClass):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    short_description = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    logo = models.ForeignKey(Images, related_name='organizations', on_delete=models.SET_NULL, blank=True, null=True)
    banner = models.ForeignKey(
            Images,
            related_name='organization_banners',
            on_delete=models.SET_NULL,
            blank=True,
            null=True
            )
    director = models.ForeignKey( settings.AUTH_USER_MODEL, related_name='directed_organizations', on_delete=models.CASCADE)
    default_sport = models.CharField(max_length=20, choices=Sports.choices, default=Sports.BASKETBALL)

    @property
    def logo_url(self):
        if self.logo:
            return self.logo.image.url
        return "/assets/defaults/globe.webp"


    class Meta: # type: ignore
        verbose_name_plural = 'Organizations'
        ordering = ['name']

    def __str__(self):
        return str(self.name)


class Membership(ABSClass):
    class Role(models.TextChoices):
        DIRECTOR = 'director', 'Director'
        ADMIN = 'admin', 'Admin'
        STAFF = 'staff', 'Staff'
        COACH = 'coach', 'Coach'
        PARTICIPANT = 'participant', 'Participant'
        PARENT = 'parent', 'Parent'

    role = models.CharField(max_length=20, choices=Role.choices)
    selected = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='memberships', on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, related_name='memberships', on_delete=models.CASCADE)

    def select(self):
        with transaction.atomic():
            Membership.objects.filter(
                user=self.user,
                role=self.role
            ).exclude(pk=self.pk).update(selected=False)

            self.selected = True
            self.save()

    class Meta: # type: ignore
        unique_together = ('user', 'organization')

    def __str__(self):
        return f"{self.user.username} - {self.organization.name} ({self.role})"


class Team(ABSClass):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=50, blank=True, null=True)
    selected = models.BooleanField(default=False)
    logo = models.ForeignKey(Images, related_name='team_logos', on_delete=models.SET_NULL, blank=True, null=True)
    owner = models.ForeignKey(Owner, related_name='teams', on_delete=models.CASCADE, blank=True, null=True)

    @property
    def select(self):
        with transaction.atomic():
            Team.objects.filter(
                owner=self.owner,
                selected=True
            ).exclude(pk=self.pk).update(selected=False)

            self.selected = True
            self.save()

    @property
    def team_logo_url(self):
        if self.logo:
            return self.logo.image.url
        return "/assets/defaults/team-logo.png"

    def __str__(self):
        return str(self.name)


class Event(ABSClass):
    class Status(models.TextChoices):
        CREATED = 'created', 'Created'
        UPCOMING = 'upcoming', 'Upcoming'
        ONGOING = 'ongoing', 'Ongoing'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    class Type(models.TextChoices):
        PICKUP = 'pickup', 'Pickup'
        TOURNAMENT = 'tournament', 'Tournament'
        LEAGUE = 'league', 'League'
        CAMP = 'camp', 'Camp'

    name = models.CharField(max_length=255)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    short_description = models.CharField(max_length=80, blank=True)
    description = models.TextField(max_length=255, blank=True)
    event_type = models.CharField(max_length=20, choices=Type.choices, default=Type.PICKUP)
    poster = models.ForeignKey(Images, related_name='event_posters', on_delete=models.SET_NULL, blank=True, null=True)
    price = models.IntegerField(verbose_name='Price (in cents)', default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CREATED)
    organization = models.ForeignKey(Organization, related_name='events', on_delete=models.CASCADE)
    sport = models.CharField(max_length=20, choices=Sports.choices)

    @property
    def poster_url(self):
        if self.poster:
            return self.poster.image.url
        return "/assets/defaults/event.webp"

    def save(self, *args, **kwargs):
        if not self.sport:
            self.sport = self.organization.default_sport
        super().save(*args, **kwargs)


class Address(ABSClass):
    name = models.CharField(max_length=255)
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='addresses', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.country}"


class Venue(ABSClass):
    name = models.CharField(max_length=255)
    address = models.ForeignKey(Address, related_name='locations', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='locations', on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.event.name} - {self.address.name}"


class DivisionInfo(ABSClass):
    class Gender(models.TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'

    class Level(models.TextChoices):
        BEGINNER = 'beginner', 'Beginner'
        INTERMEDIATE = 'intermediate', 'Intermediate'
        ADVANCED = 'advanced', 'Advanced'
        ELITE = 'elite', 'Elite'
        BRONZE = 'bronze', 'Bronze'
        SILVER = 'silver', 'Silver'
        GOLD = 'gold', 'Gold'
        PLATINUM = 'platinum', 'Platinum'
        JV = 'jv', 'Junior Varsity'
        VARSITY = 'varsity', 'Varsity'
        CLUB = 'club', 'Club'

    gender  = models.CharField(max_length=20, choices=Gender.choices)
    level = models.CharField(max_length=21, choices=Level.choices)
    age = models.IntegerField(verbose_name='Age (in years)')

    @property
    def name(self):
        return f"{ self.gender } (O/U) { self.age } [{ self.level }]"


class DivisionOrg(ABSClass):
    info = models.ForeignKey(DivisionInfo, related_name='division_orgs', on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, related_name='divisions', on_delete=models.CASCADE)


class DivisionEvent(ABSClass):
    info = models.ForeignKey( DivisionInfo, related_name='division_events', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='divisions', on_delete=models.CASCADE)


class DivisionTeam(ABSClass):
    info = models.ForeignKey(DivisionInfo, related_name='division_team', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name='divisions', on_delete=models.CASCADE,)


class Registration(ABSClass):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PENDING = 'pending', 'Pending'
        CANCELLED = 'cancelled', 'Cancelled'
        REGISTERED = 'registered', 'Registered'
        COMPLETED = 'completed', 'Completed'

    registration_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    payment_status = models.BooleanField(default=False)
    payment_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    event = models.ForeignKey(Event, related_name='registrations', on_delete=models.CASCADE)
    owner = models.ForeignKey(
            Owner,
            related_name='registrations',
            on_delete=models.CASCADE,
            blank=True,
            null=True
            )

    @property
    def reported_division_ids(self):
        return self.entries.values_list('reported_division__id', flat=True)


class Entry(ABSClass):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELLED = 'cancelled', 'Cancelled'
        REJECTED = 'rejected', 'Rejected'
        ASSIGNED = 'assigned', 'Assigned'

    status = models.CharField( max_length=20, choices=Status.choices, default=Status.PENDING)
    registration = models.ForeignKey( Registration, related_name='entries', on_delete=models.CASCADE)
    team = models.ForeignKey( Team, related_name='team', on_delete=models.CASCADE)
    reported_division = models.ForeignKey(DivisionInfo, related_name='entries', on_delete=models.CASCADE)
    assigned_division = models.ForeignKey(
            DivisionInfo,
            related_name='registration_entries',
            on_delete=models.SET_NULL,
            blank=True,
            null=True
            )

    @property
    def name(self):
        return f"{ self.team.name }  { self.reported_division.gender } (O/U) {self.reported_division.age} [{ self.reported_division.level }]"


class Game(ABSClass):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        SCHEDULED = 'scheduled', 'Scheduled'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED)
    team1_score = models.IntegerField(default=0, help_text='Score for Team 1')
    team2_score = models.IntegerField(default=0, help_text='Score for Team 2')
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    play_area = models.CharField(max_length=255, blank=True, null=True)
    game_number = models.CharField(max_length=20, blank=True, null=True)
    venue = models.ForeignKey(Venue, related_name='games', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='games', on_delete=models.CASCADE)
    division = models.ForeignKey(DivisionInfo, related_name='games', on_delete=models.CASCADE)
    team1 = models.ForeignKey(Entry, related_name='team1_games', on_delete=models.CASCADE)
    team2 = models.ForeignKey(Entry, related_name='team2_games', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.event.name} - {self.team1.name} vs {self.team2.name}"


