from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .forms import RegistrationForm, HouseholdForm, HouseholdInviteForm, UpdateUserForm
from .models import HouseholdModel


def index(request):
    households = []
    if request.user.is_authenticated:
        households = HouseholdModel.objects.filter(members__id=request.user.id)
    
    context = {
        'households': households,
    }
    return render(request, 'home.html', context=context)


# Register
def register_view(request):
    if request.method == 'POST':
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

@login_required
def household_view(request):
    if request.method == 'POST':
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

@login_required
def household_invite_view(request):
    if request.method == 'POST':
        form = HouseholdInviteForm(request.user, request.POST)
        if form.is_valid():
            invite = form.save(request)

    else:
        form = HouseholdInviteForm(request.user)

    context = {
        'title': 'Invite a User',
        'form': form,
    }

    return render(request, 'household_invite.html', context=context)

@login_required
def profile_view(request):
    households = HouseholdModel.objects.filter(members__id=request.user.id)
    context = {
        'user': request.user,
        'households': households,
    }

    return render(request, 'profile.html', context=context)

@login_required
def update_profile_view(request):
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/profile')

    else:
        form = UpdateUserForm(instance=request.user)

    context = {
        'form': form,
    }

    return render(request, 'registration/update_profile.html', context=context)