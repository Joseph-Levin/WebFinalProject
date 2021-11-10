from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponse

from .forms import RegistrationForm, HouseholdForm


def index(request):
    context = {
        'name': 'Joseph',
    }
    return render(request, 'home.html', context=context)


# Register
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

    return render(request, 'registration/register.html', context=context)

# Logout
def logout_view(request):
    logout(request)
    return redirect('/login/')

def household_view(request):
    if request.method == "POST":
        form = HouseholdForm(request.POST)
        if form.is_valid():
            household = form.save(request)
            household.members.add(request.user)
            redirect('/household/'+ household.name)

    else:
        form = HouseholdForm()

    context = {
        'title': 'Add a Household',
        'form': form,
    }

    return render(request, 'household.html', context=context)