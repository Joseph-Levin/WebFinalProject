from typing import List
from django.core import serializers
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings

from .forms import RegistrationForm, HouseholdForm, HouseholdInviteForm, UpdateUserForm, ListItemForm
from .models import HouseholdInviteModel, HouseholdModel, ListItemModel, ListModel


def index(request):
    households = []
    if request.user.is_authenticated:
        households = HouseholdModel.objects.filter(members__id=request.user.id)
    
    context = {
        'households': households,
        'default_icon': settings.MEDIA_URL+'icons/default_icon.jpg',

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

    return render(request, 'view_households.html', context=context)

@login_required
def household_invite(request, id):
    if request.method == 'POST':
        form = HouseholdInviteForm(request.POST, userid=request.user.id, houseid=id)
        if form.is_valid():
            invite = form.save(request)
            return redirect('/household/'+ str(id))

    else:
        form = HouseholdInviteForm(userid=request.user.id, houseid=id)
        
    context = {
        'title': 'Invite a User',
        'form': form,
        'id': id,
    }
    return render(request, 'household/invite.html', context=context)



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

@login_required
def household_home(request, id):
    household = HouseholdModel.objects.get(pk=id)
    lists = ListModel.objects.filter(household=id)

    context = {
        'household': household,
        'lists': lists,
    }

    return render(request, 'household/home.html', context=context)

@login_required
def view_list(request, id, listid):
    list = ListModel.objects.get(pk=listid)
    listitems = ListItemModel.objects.filter(list=listid)

    if request.method == 'POST':
        form = ListItemForm(request.POST, userid=request.user.id, listid=listid)
        if form.is_valid():
            form.save()
    else:
        form = ListItemForm(userid=request.user.id, listid=listid)
    
    context = {
        'form': form,
        'list': list,
        'listitems': listitems,
    }

    return render(request, 'household/list/list.html', context=context)

@login_required
def list_item_toggle(request, id, listid, itemid):
    list_item = ListItemModel.objects.get(pk=itemid)
    list_item.complete = not list_item.complete
    list_item.save()

    return redirect('/household/'+str(id)+'/list/'+str(listid))

@login_required
def list_item_delete(request, id, listid, itemid):
    list_item = ListItemModel.objects.get(pk=itemid)
    list_item.delete()

    return redirect('/household/'+str(id)+'/list/'+str(listid))

@login_required
def list_item_edit(request, id, listid, itemid):
    list_item = ListItemModel.objects.get(pk=itemid)
    if request.method == 'POST':
        form = ListItemForm(request.POST, instance=list_item)
        if form.is_valid():
            form.save()
            return redirect('/household/'+str(id)+'/list/'+str(listid))
    
    else:
        form = ListItemForm(instance=list_item)

    return render(request, 'household/list/listitem.html', {'id': id, 'listid': listid, 'form': form})


def list_json(request, listid):
    list = ListModel.objects.get(pk=listid)
    list_items = ListItemModel.objects.filter(list=listid)
    data = serializers.serialize('json', list_items)

    return HttpResponse(data)