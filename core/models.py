from django.db import models
from django.conf import settings


class Organization(models.Model):
    name = models.CharField(max_length=255)


class Role(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    COACH = 'coach', 'Coach'
    WORKER = 'worker', 'Worker'


class Membership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=Role.choices)

    class Meta:
        unique_together = ('user', 'organization')
