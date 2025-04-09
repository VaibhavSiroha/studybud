from django.shortcuts import render
from .models import Room
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
