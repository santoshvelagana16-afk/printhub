from django.shortcuts import render, redirect
from django.contrib import messages
from services.models import Service


def home(request):
    services = Service.objects.filter(is_active=True)[:6]
    return render(request, 'home.html', {'services': services})


def contact(request):
    if request.method == 'POST':
        messages.success(request, 'Thank you! Your message has been sent. We will get back to you shortly.')
        return redirect('contact')
    return render(request, 'contact.html')
