from django.shortcuts import render
from .models import Message
from main.models import HouseholdModel


def index(request):
    return render(request, 'chat/index.html')

def room(request, room_name):

    username = str(request.user)
    messages = Message.objects.filter(household=room_name)
    household_name = HouseholdModel.objects.get(id=room_name).name
    print(household_name)

    context = {
        'room_name': room_name,
        'username': username,
        'messages': messages,
        'household_name': household_name,
    }

    return render(request, 'chat/room.html', context=context)