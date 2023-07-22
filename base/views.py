from django.shortcuts import render , redirect
from django.http import HttpResponse 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from .models import Room , Topic,Message
from .forms import RoomForm , UserForm
# Create your views here.
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Password is Incorrect')
        except:
            messages.error(request, 'User Does Not Exist or Incorrect Username')

        

        

    context = {'page':page}
    return render(request, 'base/loginOrRegister.html', context)

def logout_user(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    page = 'register'
    form = UserCreationForm()
    context = {'page':page , 'form':form}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
             messages.error(request, 'An error occured ! Please Retry')
    return render(request,'base/loginOrRegister.html', context )

def home(request):
    if request.GET.get('q') != None:
        q = request.GET.get('q')
    else:
        q = ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    topics = Topic.objects.all()  
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms':rooms , 'topics':topics, 'room_count' : room_count, 'room_messages':room_messages}
    return render(request, 'base/home.html', context)

def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user' : user , 'rooms':rooms ,'room_messages':room_messages , 'topics':topics}
    return render(request, 'base/profile.html', context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    rmessages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get("body")
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room' : room , 'rmessages':rmessages, 'participants':participants}
    return render(request, 'base/room.html' , context)

@login_required(login_url='login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)

    if request.user!=message.user:
        return HttpResponse('You are not allowed here')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request,'base/delete.html', {'obj':message})

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    # if request.method == 'POST':
    #     form = RoomForm(request.POST)
    #     if form.is_valid():
    #         room = form.save(coomit=False)
    #         room.host = request.user
    #         room.save()
    #         return redirect('home')
    
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        topic = request.POST.get('topic')
        room_about = request.POST.get('room_about')
        topic_obj = Topic(name=topic)
        topic_obj.save()
        room_obj = Room(topic=topic_obj,host=request.user,name=room_name,description=room_about)
        room_obj.save()
        return redirect('home')

    context = {}
    return render(request, 'base/room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    room_name = room.name
    topic = room.topic
    about = room.description

    if request.user!=room.host:
        return HttpResponse('You are not allowed here')

    if request.method=='POST':
        room_name = request.POST.get('room_name')
        topic = request.POST.get('topic')
        room_about = request.POST.get('room_about')
        room.name = room_name
        topic_obj = room.topic
        topic_obj.name = topic
        topic_obj.save()
        room.topic = topic_obj
        room.description = room_about
        room.save()
        return redirect('home')
        
    context = {'room':room,'room_name':room_name,'topic':topic,'about':about}
    return render(request, 'base/room_form_update.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)

    if request.user!=room.host:
        return HttpResponse('You are not allowed here')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html', {'obj':room})

@login_required(login_url='login')
def profileUpdate(request,pk):
    user = request.user
    form = UserForm(instance=user)

    if request.method=='POST':
        form = UserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile',pk=user.id)
    context = {'user':user,'form':form}
    return render(request,'base/profile_update.html',context)