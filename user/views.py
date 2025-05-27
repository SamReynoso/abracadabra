from django.shortcuts import render


def register(request):
    return render(request, 'core/register.html')


def login(request):
    return render(request, 'core/login.html')


def billing(request):
    return render(request, 'core/billing.html')


def settings(request):
    return render(request, 'core/settings.html')
