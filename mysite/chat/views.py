from django.shortcuts import render


def index(request):
    return render(request, 'chat/index.html')

def room(request, room_name):

    username = str(request.user)

    return render(request, 'chat/room.html', { 'room_name': room_name, 'username': username })