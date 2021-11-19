from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings

from .forms import RegistrationForm, HouseholdForm, HouseholdInviteForm, UpdateUserForm
from .models import HouseholdInviteModel, HouseholdModel


def index(request):
    households = []
    if request.user.is_authenticated:
        households = HouseholdModel.objects.filter(members__id=request.user.id)
    
    context = {
        'households': households,
    }
    return render(request, 'home.html', context=context)


# Register
def register(request):
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
def household(request):
    if request.method == 'POST':
        form = HouseholdForm(request.POST, request.FILES)
        if form.is_valid():
            household = form.save(request)
            household.members.add(request.user)
            redirect('/household/'+ household.name)

    else:
        form = HouseholdForm()

    households = HouseholdModel.objects.filter(members__id=request.user.id)

    context = {
        'title': 'Add a Household',
        'form': form,
        'households': households,
        'default_icon': settings.MEDIA_URL+'icons/default_icon.jpg',
    }

    return render(request, 'household.html', context=context)

@login_required
def household_invite(request):
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
def profile(request):
    households = HouseholdModel.objects.filter(members__id=request.user.id)
    invites = HouseholdInviteModel.objects.filter(invitee=request.user)
    context = {
        'user': request.user,
        'households': households,
        'invites': invites,
    }

    return render(request, 'profile.html', context=context)

@login_required
def update_profile(request):
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

@login_required
def accept_invite(request, id):
    household = HouseholdModel.objects.get(pk=id)
    household.members.add(request.user)
    invite = HouseholdInviteModel.objects.get(invitee=request.user, household=id)
    invite.delete()
    return redirect('/')


@login_required
def decline_invite(request, id):
    HouseholdInviteModel.objects.get(pk=id).delete()

    return redirect(profile)


@login_required
def leave_household(request, id):
    household = HouseholdModel.objects.get(pk=id)
    household.members.remove(request.user)

    if household.members.count() == 0:
        household.delete()

    return redirect('/')