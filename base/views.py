from django.shortcuts import render,redirect
from .models import Room
from .forms import RoomForm
'''
rooms=[
    {'id':1,'name':'Lets learn python'},
    {'id':2,'name':'Design With Me'},
    {'id':3,'name':'Breaking Bihar'},
]
'''

def home(requset):
    rooms=Room.objects.all()
    context={'rooms':rooms}
    return render(requset,'base/home.html',context)

def room(requset,pk):
    room= Room.objects.get(id=pk)
    context={'room': room}
    return render(requset,'base/room.html',context)

def createRoom(request):
    form=RoomForm()
    if request.method=='POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'base/room_form.html',context)