from django.shortcuts import render


def register(request):
    return render(request, 'user/register.html')


def login(request):
    return render(request, 'user/login.html')


def billing(request):
    return render(request, 'user/billing.html')


def settings(request):
    return render(request, 'user/settings.html')

def profile(request):
    return render(request, 'user/profile.html')
