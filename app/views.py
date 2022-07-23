from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib import messages
from .models import Room,Topic
from .forms import roomform


def loginpage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"user doesn't exist")
    context ={}
    return render(request,'app/login.html',context)


      
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ' '
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(desc__icontains=q))
        
    topics = Topic.objects.all()
    context = {'rooms':rooms,'topics':topics }
    return render(request, 'app/home.html',context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'app/room.html',context)

def createroom(request):
    form = roomform()
    if request.method == 'POST':
        form = roomform(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('home')
        
    context= {'form':form}
    return render(request,'app/room_form.html',context)

def updateroom(request,pk):
    room =Room.objects.get(id=pk)
    form = roomform(instance=room)
    if form.is_valid():
        form.save()
        return redirect('home')

    context= {'form':form}
    return render(request,'app/room_form.html',context) 

def deleteroom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'app/delete.html',{'obj':room})
