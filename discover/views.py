from django.shortcuts import render


def marketplace(request):
    return render(request, 'discover/marketplace.html')

def event_details(request):
    return render(request, 'discover/event-details.html')

def event_register(request):
    return render(request, 'discover/event-register.html')

def org(request):
    return render(request, 'discover/org-details.html')

def dashboard(request):
    return render(request, 'discover/dashboard.html')

def persona(request):
    return render(request, 'discover/persona-details.html')

