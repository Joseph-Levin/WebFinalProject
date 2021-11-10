from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponse

from .forms import RegistrationForm


def index(request):
    context = {
        'name': 'Joseph',
    }
    return render(request, 'home.html', context=context)


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save(request)
            return redirect('/')

    else:
        form = RegistrationForm()

    context = {
        'title': 'Registration Page',
        'form': form,
    }

    return render(request, 'register.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('/login/')
