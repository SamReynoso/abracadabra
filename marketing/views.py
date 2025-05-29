from django.shortcuts import render


def landing(request):
    return render(request, 'marketing/landing.html')

def billpay(request):
    return render(request, 'marketing/billpay.html')



def demo(request):
    return render(request, 'marketing/demo.html')
