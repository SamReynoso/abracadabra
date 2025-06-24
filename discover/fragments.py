from django.shortcuts import render
from django.core.paginator import Paginator
from models.models import (
        Event,
        Team,
        Registration,
        )


def guest_contact_info(request, guest):
    context = { 'guest': guest }
    return render(request, 'discover/fragments/contact_info.html', context)


def guest_contact_info_form(request, guest):
    context = { 'guest': guest }
    return render(request, 'discover/fragments/contact_info_form.html', context)

def workspace_content(request, owner):
    context = {
        'owner': owner,
        'teams': Team.objects.filter(owner=owner),
        'registrations': Registration.objects.filter(owner=owner),
    }
    return render(request, 'discover/fragments/workspace_content.html', context)


def teams(request, owner):
    context = {
        'teams': Team.objects.filter(owner=owner),
        'registrations': Registration.objects.filter(owner=owner),
    }
    return render(request, 'discover/fragments/teams.html', context)


def registrations_cancel(request, registration):
    context = { 'registrations': registration }
    return render(request, 'discover/fragments/registrations_cancel.html', context)


def division_form(request, team):
    context = { 'team': team }
    return render(request, 'discover/fragments/division_form.html', context)


def handle_team_update(request, team):
    context = {
            'team': team,
            'registrations': Registration.objects.filter(owner=team.owner)
               }
    return render(request, 'discover/fragments/handle_team_update.html', context)

def handle_division_update(request, team):
    context = {
            'team': team,
            'registrations': Registration.objects.filter(owner=team.owner)
               }
    return render(request, 'discover/fragments/handle_division_update.html', context)

def registration_form(request, registration):
    context = { 'registration': registration }
    if registration.status == Registration.Status.DRAFT:
        print("Rendering registration form for draft registration")
        return render(request, 'discover/fragments/registration_form.html', context)
    return render(request, 'discover/fragments/registration_details.html', context)


def registration_cancel(request, registration):
    context = { 'registration': registration }
    return render(request, 'discover/fragments/registration_cancel.html', context)


def team_form(request, team):
    context = { 'team': team, }
    return render(request, 'discover/fragments/team_form.html', context)


def team_delete_form(request, team):
    context = { 'team': team, }
    return render(request, 'discover/fragments/team_delete_form.html', context)


def basketball_spotlight(request, page_number: str):
    page = int(page_number)
    events = Event.objects.all()
    paginator = Paginator(events, 3)
    if page < 1 or page > paginator.num_pages:
        page_obj = None
    else:
        page_obj = paginator.get_page(page_number)
    context = {
        'events': page_obj,
        'next_page': page + 1 if int(page) < paginator.num_pages else None,
    }
    return render(request, 'discover/result_paginator.html', context)

