from django.shortcuts import redirect, render
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm 
from .models import Room,Topic
from .forms import roomform


def loginpage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"")
        
        user = authenticate(request,username=username,password=password)

        if user is not None: 
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'username or password does not exist')
    
    context ={'page':page}
    return render(request,'app/login.html',context)


def logoutuser(request):
    logout(request)
    return redirect('home')

def reguser(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'unexpected error')

    return render(request, 'app/login.html',{'form':form})
      
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
    messages = room.message_set.all().order_by('-created')
    context = {'room': room,'messages':messages}
    return render(request, 'app/room.html',context)

@login_required(login_url='login')
def createroom(request):
    form = roomform()
    if request.method == 'POST':
        form = roomform(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('home')
        
    context= {'form':form}
    return render(request,'app/room_form.html',context)


@login_required(login_url='login')
def updateroom(request,pk):
    room = Room.objects.get(id=pk)
    form = roomform(instance=room)

    if request.user != room.host:
        return HttpResponse('not allowed here!!')

    if form.is_valid():
        form.save()
        return redirect('home')

    context= {'form':form}
    return render(request,'app/room_form.html',context) 

@login_required(login_url='login')
def deleteroom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'app/delete.html',{'obj':room})
