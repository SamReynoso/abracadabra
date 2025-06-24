from models.models import Images, Event
from django.shortcuts import render


def image_upload_form(request):
    return render(request, "app/fragment/upload_image_form.html") # This is renamed and will break if the file name is not updated

def image_form(request, image):
    context = { 'image': image }
    return render(request, "app/fragments/image_form.html", context)

def image_delete_form(request, image): 
    context = { 'image': image }
    return render(request, "app/fragment/upload_image_form.html", context) # This is not the right template for this view


def images(request, images):
    context = { 'images': images }
    return render(request, "app/fragments/images.html", context)


def event_card(request, event):
    context = { 'event': event }
    return render(request, "app/fragments/event_card.html", context)

def event_details(request, event):
    context = { 'event': event }
    return render(request, "app/fragments/event_details.html", context)

def event_form(request, event, form):
    context = { "event": event, "form": form }
    return render(request, "app/fragments/event_form.html", context)

def event_poster_select(request, event, images):
    context = { "event": event, "images": images }
    return render(request, "app/fragments/event_poster_select.html", context)

def event_poster_accept(request, event, image):
    context = { "event": event, "image": image }
    return render(request, "app/fragments/event_poster_accept.html", context)

def event_venue_form(request, event):
    context = { "event": event }
    return render(request, "app/fragments/event_venue_form.html", context)

def event_delete_form(request, event):
    context = { "event": event, }
    return render(request, "app/fragments/event_delete.html", context)



def manage_registrations(request, event, registrations): # This is renamed and will break if not updated where this is called
    context = { "event": event, "registrations": registrations }
    return render(request, "app/fragments/manage_registrations.html", context) # This is renamed and will break if the file name is not updated



def entry_card(request, entry):
    context = { "entry": entry }
    return render(request, "app/fragments/entry_card.html", context)

def entry_details(request, entry):
    context = { "entry": entry }
    return render(request, "app/fragments/entry_details.html", context)

def entry_assign_form(request, entry):
    context = { "entry": entry }
    return render(request, "app/fragments/entry_assign_form.html", context)

def entry_confirm_form(request, entry):
    context = { "entry": entry }
    return render(request, "app/fragments/entry_confirm_form.html", context)

def entry_reject_form(request, entry):
    context = { "entry": entry }
    return render(request, "app/fragments/entry_reject_form.html", context)


def manage_division_form(request, division):
    context = { "division": division }
    return render(request, "app/fragments/manage_division_form.html", context)
