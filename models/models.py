import numpy as np
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models, transaction

class Role(models.TextChoices):
    DIRECTOR = 'director', 'Director'
    ADMIN = 'admin', 'Admin'
    STAFF = 'staff', 'Staff'
    COACH = 'coach', 'Coach'
    PARTICIPANT = 'participant', 'Participant'
    PARENT = 'parent', 'Parent'


class EventType(models.TextChoices):
    PICKUP = 'pickup', 'Pickup'
    TOURNAMENT = 'tournament', 'Tournament'
    LEAGUE = 'league', 'League'
    CAMP = 'camp', 'Camp'


class EventStatus(models.TextChoices):
    CREATED = 'created', 'Created'
    UPCOMING = 'upcoming', 'Upcoming'
    ONGOING = 'ongoing', 'Ongoing'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'


class RegistrationStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    PENDING = 'pending', 'Pending'
    CANCELLED = 'cancelled', 'Cancelled'
    REGISTERED = 'registered', 'Registered'
    COMPLETED = 'completed', 'Completed'


class ABSClass(models.Model):
    """
    Abstract base class for models that require a primary field.
    """
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
        """
        Create an instance from a slug.
        """
        pk = str(slug)
        try:
            return cls.objects.get(pk=pk)
        except cls.DoesNotExist:
            raise ValueError(
                    f"{cls.__name__} with slug '{slug}' does not exist."
                    )

    class Meta:
        abstract = True


class User(AbstractUser):
    profile_picture = models.ImageField(
            upload_to='profile_pictures/',
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


class Images(ABSClass):
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            related_name='images',
            on_delete=models.CASCADE,
            blank=True,
            null=True
            )
    image = models.ImageField(
            upload_to='user_images/',
            )
    caption = models.CharField(max_length=255, blank=True)
    is_profile_picture = models.BooleanField(default=False)


    @property
    def display_name(self):
        return "foobar"


class Organization(ABSClass):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    short_description = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    logo = models.ForeignKey(
            Images,
            related_name='organizations',
            on_delete=models.SET_NULL,
            blank=True,
            null=True
            )
    banner = models.ForeignKey(
            Images,
            related_name='organization_banners',
            on_delete=models.SET_NULL,
            blank=True,
            null=True
            )

    @property
    def logo_url(self):
        """
        Return the URL of the organization's logo image.
        """
        if self.logo:
            return self.logo.image.url
        return "/assets/defaults/globe.svg"


    class Meta: # type: ignore
        verbose_name_plural = 'Organizations'
        ordering = ['name']

    def __str__(self):
        return str(self.name)



class Membership(ABSClass):
    role = models.CharField(max_length=20, choices=Role.choices)
    primary = models.BooleanField(default=False)
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            related_name='memberships',
            on_delete=models.CASCADE
            )
    organization = models.ForeignKey(
            Organization,
            related_name='memberships',
            on_delete=models.CASCADE
            )

    def set_primary(self):
        """
        Atomically set this membership as primary and unset others.
        """
        with transaction.atomic():
            Membership.objects.filter(
                user=self.user,
                role=self.role
            ).exclude(pk=self.pk).update(primary=False)

            self.primary = True
            self.save()

    class Meta: # type: ignore
        unique_together = ('user', 'organization')

    def __str__(self):
        return f"{self.user.username} - {self.organization.name} ({self.role})"


class Address(ABSClass):
    name = models.CharField(max_length=255)
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            related_name='addresses',
            on_delete=models.CASCADE,
            blank=True,
            )
    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.country}"



class Event(ABSClass):
    name = models.CharField(max_length=255)
    event_type = models.CharField(
            max_length=20,
            choices=EventType.choices,
            default=EventType.PICKUP
            )
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    short_description = models.CharField(max_length=80, blank=True)
    description = models.TextField(max_length=255, blank=True)

    poster = models.ForeignKey(
            Images,
            related_name='event_posters',
            on_delete=models.SET_NULL,
            blank=True,
            null=True
            )

    @property
    def poster_url(self):
        """
        Return the URL of the event poster image.
        """
        if self.poster:
            return self.poster.image.url
        return "/assets/defaults/event-poster.png"

    price = models.IntegerField(
            verbose_name='Price (in cents)',
            default=0
            )
    status = models.CharField(
            max_length=20,
            choices=EventStatus.choices,
            default=EventStatus.CREATED
            )
    organization = models.ForeignKey(
            Organization,
            related_name='events',
            on_delete=models.CASCADE
            )


    @property
    def director(self):
        membership = self.organization.memberships.filter(
            role=Role.DIRECTOR,
        ).first()
        if membership:
            return membership.user
        return None

    @property
    def currency(self) -> float:
        return np.round(self.price / 100, 2)

    @property
    def display_location(self):
        locations = self.locations.all()
        if locations.exists():
            first  = locations.first()
            return f"{first.address.city}, {first.address.state}, {first.address.country}"
        return None

    @property
    def formatted_price(self) -> str:
        return f"${self.currency:.2f}"

    def set_price(self, price: float | int | str) -> None:
        if isinstance(price, str):
            if price.startswith('$'):
                price = price[1:]
            if price.count('.') == 1:
                self.price = int(price.replace('.', ''))
            else:
                self.price = int(price) * 100

        elif isinstance(price, int):
            self.price = price * 100

        elif isinstance(price, float):
            value = price * 100
            if value != int(value):
                raise ValueError("Price must be a whole number of cents.")
            self.price = int(value)


    def __str__(self):
        return str(self.name)


class Location(ABSClass):
    address = models.ForeignKey(
            Address,
            related_name='locations',
            on_delete=models.CASCADE,
            blank=True,
            null=True
            )
    event = models.ForeignKey(
            Event,
            related_name='locations',
            on_delete=models.CASCADE,
            blank=True,
            null=True
            )
    def __str__(self):
        return f"{self.event.name} - {self.address.name}"


class DivisionGender(models.TextChoices):
    MALE = 'male', 'Male'
    FEMALE = 'female', 'Female'

class DivisionLevel(models.TextChoices):
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


class DivisionInfo(ABSClass):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=50, blank=True, null=True)
    gender  = models.CharField(
            max_length=20,
            choices=DivisionGender.choices,
            )
    level = models.CharField(
            max_length=20,
            choices=DivisionLevel.choices,
            )
    age = models.IntegerField(
            verbose_name='Age (in years)',
            default=0,
            help_text='Age of participants in this division'
            )
    organization = models.ForeignKey(
            Organization,
            related_name='divisions',
            on_delete=models.CASCADE
            )

    def __str__(self):
        return str(self.name)

class EventDivision(ABSClass):
    event = models.ForeignKey(
            Event,
            related_name='divisions',
            on_delete=models.CASCADE
            )
    info = models.ForeignKey(
            DivisionInfo,
            related_name='event_divisions',
            on_delete=models.CASCADE,
            blank=True,
            null=True
            )

class Guest(ABSClass):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    uuid = models.UUIDField(
            default=uuid.uuid4,
            #editable=False,
            #unique=True,
            #help_text='Unique identifier for the registration'
            )

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


class Team(ABSClass):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=50, blank=True, null=True)
    logo = models.ForeignKey(
            Images,
            related_name='team_logos',
            on_delete=models.SET_NULL,
            blank=True,
            null=True
            )
    owner = models.ForeignKey(
            Owner,
            related_name='teams',
            on_delete=models.CASCADE,
            blank=True,
            null=True
            )

    @property
    def team_logo_url(self):
        if self.logo:
            return self.logo.image.url
        return "/assets/defaults/team-logo.png"

    def __str__(self):
        return str(self.name)


class TeamDivision(ABSClass):
    gender  = models.CharField(
            max_length=20,
            choices=DivisionGender.choices,
            )
    level = models.CharField(
            max_length=20,
            choices=DivisionLevel.choices,
            )
    age = models.IntegerField(
            verbose_name='Age (in years)',
            default=0,
            help_text='Age of participants in this division'
            )
    team = models.ForeignKey(
            Team,
            related_name='divisions',
            on_delete=models.CASCADE,
            )



class Registration(ABSClass):
    registration_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    payment_status = models.BooleanField(default=False)
    payment_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
            max_length=20,
            choices=RegistrationStatus.choices,
            default=RegistrationStatus.DRAFT
            )
    event = models.ForeignKey(
            Event, 
            related_name='registrations',
            on_delete=models.CASCADE
            )
    owner = models.ForeignKey(
            Owner,
            related_name='registrations',
            on_delete=models.CASCADE,
            blank=True,
            null=True
            )


class RegistrationEntryStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    CONFIRMED = 'confirmed', 'Confirmed'
    CANCELLED = 'cancelled', 'Cancelled'
    REJECTED = 'rejected', 'Rejected'
    ASSIGNED = 'assigned', 'Assigned'


class RegistrationEntry(ABSClass):
    registration = models.ForeignKey(
            Registration,
            related_name='entries',
            on_delete=models.CASCADE
            )
    reported_division = models.ForeignKey(
            TeamDivision,
            related_name='registration_entries',
            on_delete=models.CASCADE,
            )
    assigned_division = models.ForeignKey(
            EventDivision,
            related_name='registration_entries',
            on_delete=models.SET_NULL,
            blank=True,
            null=True
            )
    status = models.CharField(
            max_length=20,
            choices=RegistrationEntryStatus.choices,
            default=RegistrationEntryStatus.PENDING
            )
    confirmed = models.BooleanField(default=False)
    assigned = models.BooleanField(default=False)



