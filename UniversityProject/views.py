from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message, User, Blockchain, News
from .forms import RoomForm, UserForm, UserCForm
import pandas_datareader as pdr
import datetime as dt
import plotly.graph_objects as go
from datetime import timezone
from django.core.paginator import Paginator
from pathlib import Path
import os



def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method =='POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            email = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')
    context = {'page': page}
    return render(request, 'UniversityProject/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCForm
    if request.method == 'POST':
        form = UserCForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred')

    return render(request, 'UniversityProject/login_register.html', {'form':form})

def home(request):
    blockchain = Blockchain.objects.all()[0:4]
    context = { 'blockchain':blockchain}
    return render(request, 'UniversityProject/home.html', context)

def conversationPage(request):
    page = 'conversation'
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    room_count = rooms.count()
    topics = Topic.objects.all()[0:4]
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    blockchain = Blockchain.objects.all()[0:4]
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages':room_messages, 'blockchain':blockchain, 'page':page}
    return render(request, 'UniversityProject/conversation.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room':room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'UniversityProject/room.html', context)

def userProfile(request, pk):
    blockchain = Blockchain.objects.all()
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages':room_messages, 'topics': topics, 'blockchain':blockchain}
    return render(request, 'UniversityProject/profile.html', context)

@login_required(login_url='login')
def create_room(request):
    form = RoomForm
    topics = Topic.objects.all()
    blockchain = Blockchain.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('conversation')
    context = {'form': form, 'topics':topics, 'blockchain':blockchain}
    return render(request, 'UniversityProject/room_form.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse ('You are not the owner')
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()

        return redirect('conversation')

    context = {'form': form, 'topics':topics, 'room':room}
    return render(request, 'UniversityProject/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    context = {'obj': room}
    if request.user != room.host:
        return HttpResponse ('You are not the owner')
    if request.method == 'POST':
        room.delete()
        return redirect('conversation')
    return render(request, 'UniversityProject/delete.html', context)

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    context = {'obj': message}
    if request.user != message.user:
        return HttpResponse ('You are not the owner')
    if request.method == 'POST':
        message.delete()
        return redirect('conversation')
    return render(request, 'UniversityProject/delete.html', context)


@login_required(login_url='login')
def updateUser(request):
    blockchain = Blockchain.objects.all()
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    return render(request, 'UniversityProject/update_user.html', {'form':form, 'blockchain':blockchain})

def topicPage(request):
    blockchain = Blockchain.objects.all()
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'UniversityProject/topics.html', {'topics':topics, 'blockchain':blockchain})

def activityPage(request):
    blockchain = Blockchain.objects.all()
    room_messages = Message.objects.all()
    return render(request, 'UniversityProject/activity.html', {'room_messages':room_messages, 'blockchain':blockchain})

def blockchainFeed(request, pk):
    BASE_DIR = Path(__file__).resolve().parent.parent
    cryptocurrency = Blockchain.objects.get(id=pk)
    blockchain = Blockchain.objects.all()[0:4]
    diff = checkDiff(cryptocurrency.timeframe)
    checkpath = BASE_DIR / 'UniversityProject/templates/UniversityProject/CryptoFeed' / (cryptocurrency.short + '.html')
    say =checkpath.exists()
    if say == False:
        file = open(cryptocurrency.short + '.html', 'w')
        file.close()
        os.replace(BASE_DIR / 'USDC.html', checkpath)
    checkpath.touch(exist_ok=True)
    if diff > 28800:
        get_data(cryptocurrency.short)
        cryptocurrency.timeframe = dt.datetime.now(timezone.utc)
        cryptocurrency.save()
    path = 'UniversityProject/Crypto/' + cryptocurrency.short +'.html'
    path2 = 'UniversityProject/CryptoFeed/' + cryptocurrency.short +'.html'
    context = {'cryptocurrency':cryptocurrency, 'blockchain':blockchain, 'path':path, 'path2':path2}
    return render(request, 'UniversityProject/feed.html', context)

def newsPage(request):
    news = News.objects.all()
    blockchain = Blockchain.objects.all()[0:4]
    context = {'blockchain':blockchain, 'news':news}
    return render(request, 'UniversityProject/news.html', context)

def cryptoPage(request):
    page = 'blockchain'
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    blockch = Blockchain.objects.filter(Q(cryptocurrency__icontains=q) | Q(short__icontains=q))
    paginate_by = request.GET.get('paginate_by', 5)
    paginator = Paginator(blockch, paginate_by)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = { 'page':page, 'blockch':blockch, 'page_obj':page_obj}
    return render(request, 'UniversityProject/crypto_site.html', context)

def blockchainPage(request):
    blockchain = Blockchain.objects.all()[0:4]
    context = {'blockchain': blockchain}
    return render(request, 'UniversityProject/blockchain.html', context)


def checkDiff(timedata):
    current = dt.datetime.now(timezone.utc)
    diff = (current - timedata).total_seconds()
    return diff

def get_data(curr):
    crypto_currency = curr
    against_currency = 'GBP'

    start = dt.datetime(2016, 1, 1)
    end = dt.datetime.now()

    data = pdr.DataReader(f'{crypto_currency}-{against_currency}', 'yahoo', start, end)

    trace1 = {
        'x': data.index,
        'open': data.Open,
        'close': data.Close,
        'high': data.High,
        'low': data.Low,
        'type': 'candlestick',
        'name': 'Crypto',
        'showlegend': False
    }

    data = [trace1]
    # Config graph layout
    layout = go.Layout({
        'title': {
            'text': str(curr) +' ' +  against_currency,
            'font': {
                'size': 15
            }
        }
    })

    path = 'UniversityProject/templates/UniversityProject/Crypto/' + str(curr) + '.html'
    fig = go.Figure(data=data, layout=layout)
    fig.write_html(path)

