from django.shortcuts import render

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter




def home(request):
    print("callback ------->", GoogleOAuth2Adapter(request).get_callback_url(request, None))
    return render(request, "core/home.html")


def index(request):
    return render(request, "core/index.html")
