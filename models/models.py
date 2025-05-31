from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


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
    UPCOMING = 'upcoming', 'Upcoming'
    ONGOING = 'ongoing', 'Ongoing'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'


class RegistrationStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    CANCELLED = 'cancelled', 'Cancelled'
    REGISTERED = 'registered', 'Registered'
    COMPLETED = 'completed', 'Completed'


class User(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """
    # Add any additional fields or methods here if needed
    pass


class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    short_description = models.CharField(max_length=255, blank=True, null=True)
    poster = models.ImageField(upload_to='organization_posters/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    primary = models.BooleanField(default=False)

    def set_primary(self):
        """
        Set this organization as primary and unset others.
        """
        Organization.objects.filter(primary=True).update(primary=False)
        self.primary = True
        self.save()

    class Meta:
        verbose_name_plural = 'Organizations'
        ordering = ['name']

    def __str__(self):
        return str(self.name)


class Membership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=Role.choices)
    primary = models.BooleanField(default=False)

    def set_primary(self):
        """
        Set this membership as primary and unset others.
        """
        Membership.objects.filter(user=self.user, organization=self.organization).update(primary=False)
        self.primary = True
        self.save()

    class Meta:
        unique_together = ('user', 'organization')

    def __str__(self):
        return f"{self.user.username} - {self.organization.name} ({self.role})"


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    short_description = models.CharField(max_length=255, blank=True, null=True)
    event_type = models.CharField(max_length=20, choices=EventType.choices)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    poster = models.ImageField(upload_to='event_posters/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=EventStatus.choices, default=EventStatus.UPCOMING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class Registration(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=RegistrationStatus.choices, default=RegistrationStatus.PENDING)
    notes = models.TextField(blank=True, null=True)
    payment_status = models.BooleanField(default=False)
    payment_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def from_user(user: User, **kwargs):
        """
        Create a Registration instance from a User instance.
        """
        return Registration(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            user=user,
            **kwargs
        )

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.event.name}"


def user_has_role(user: User, org: Organization, role: Role | str) -> bool:
    return Membership.objects.filter(user=user, organization=org, role=role).exists()

