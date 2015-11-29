from django.shortcuts import get_object_or_404, render
from django.template import Template, Context
from django.http import HttpResponse
from .forms import *
from datetime import datetime
from .models import Memory
from .models import UserProfile

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as a_login
from django.contrib.auth import logout as a_logout

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

def profiletest(request, user_id):
	u = User.objects.get(pk=user_id)
	output = ("<h1>You're looking at user %s.</h1>" % user_id)
	output = output + "<br>" + u.first_name + " " + u.last_name
	return HttpResponse(output)

def userlist(request):
	lastest_user_list = User.objects.order_by('pk')[:5]
	output = ', '.join([u.username+' '+u.email for u in lastest_user_list])
	return HttpResponse(output)

def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username)
        if user is None:
            email = request.POST['email']
            if form.is_valid():
                user = User.objects.create_user(
                username=username,
                password=password,
                email=email
                )
                user.save()
                profile = UserProfile(username=username, date_created=datetime.now())
                profile.save()
                return HttpResponseRedirect('/timeline/')
        else:
            return render(request, 'signup.html', {})
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form
    })
    return render(request, 'signup.html', {})

def post(request, memory_id):
	memory = get_object_or_404(Memory, pk=memory_id)
	author = get_object_or_404(User, username=memory.author)
	return render(request, 'post.html', {'memory': memory, 'author': author, 'image' : memory.image.name[10:]})

def newpost(request):
    username = request.user.username
    return render(request, 'newpost.html', {"username": username})

def newpostsubmit(request):
    if 'title' in request.POST:
        m = Memory(name=request.POST['title'], author=request.user.username, location=request.POST['location'], date_created=datetime.now(), description=request.POST['note_text'], image=request.FILES['media'])
        m.save()
        memory = get_object_or_404(Memory, pk=m.id)
        author = get_object_or_404(User, username=memory.author)
        return post(request, m.id)
        message = 'Successfully added a new memory'
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)

def passwordreset(request):
	return render(request, 'password-reset.html', {})

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = get_object_or_404(User, email=email)
        user = authenticate(username=user.username, password=password)
        if user is not None:
            if user.is_active:
                a_login(request, user)
        else:
            return settings(request)        
        # a_login(request, user)
        return timeline(request)
    
    return render(request, 'login.html', {})

def logout(request):
    a_logout(request)
    return render(request, 'login.html', {})    

def friends(request):
	return render(request, 'friends.html', {})

def following(request):
    return render(request, 'following.html', {})

def follower(request):
    return render(request, 'follower.html', {})

def timeline(request):
    author = get_object_or_404(User, pk=1)
    memory = get_object_or_404(Memory, pk=1)
    username = request.user.username
    first_name = author.first_name
    description = memory.description
    location = memory.location
    name = memory.name
    image = memory.image
    date_created = memory.date_created
    users = User.objects.all()
    memories = Memory.objects.all()
    return render(request, 'timeline.html', {"memories": memories, "username": username})

def profilemod(request):
    author = get_object_or_404(User, username=request.user.username)
    memory = get_object_or_404(Memory, pk=1)
    username = request.user.username
    first_name = request.user.first_name
    last_name = request.user.last_name
    description = memory.description
    location = memory.location
    name = memory.name
    image = memory.image
    date_created = memory.date_created
    memories = Memory.objects.all()
    if request.method == 'POST':
        bio = get_object_or_404(UserProfile, username=request.user.username).bio
        form = BioForm(request.POST)
        bio = form.bioTextArea
        if form.is_valid():
            return HttpResponseRedirect('/Saved/')

    else:
        author = get_object_or_404(User, pk=1)
        bio = get_object_or_404(UserProfile, username=request.user.username).bio
        return render(request, 'profile-mod.html', {"bio": bio, "memories": memories, "first_name" : first_name, "username": username, "description": description, "name": name, "location": location, "image": image, "date_created": date_created})

def getUsers(request):
    users = User.objects.all()
    name_list = []
    for x in users:
        name_list.append(x.first_name + ' ' + x.last_name)
    return name_list

def getMemories(request):
    memories = Memory.objects.all()
    memory_list = []
    for x in memories:
        memorylist.append(x.first_name + ' ' + x.last_name)
    return memorylist

def location(request):
    location = {{location}}
    memories = Memory.objects.all()
    return render(request, "location.html", {"memories": memories})

def myprofile(request):
    author = get_object_or_404(User, pk=1)
    memory = get_object_or_404(Memory, pk=1)
    username = request.user.username
    first_name = request.user.first_name
    last_name = request.user.last_name
    bio = request.user.bio
    description = memory.description
    location = memory.location
    name = memory.name
    image = memory.image
    date_created = memory.date_created
    users = User.objects.all()
    memories = Memory.objects.all()
    return render(request, 'myprofile.html', {"bio": bio, "memories": memories, "first_name" : first_name, "last_name": last_name, "username": username, "description": description, "name": name, "location": location, "image": image, "date_created": date_created})

def account(request):
    author = get_object_or_404(User, pk=1)
    memory = get_object_or_404(Memory, pk=1)
    username = author.username
    first_name = author.first_name
    last_name = author.last_name
    users = User.objects.all()
    memories = Memory.objects.all()
    return render(request, 'account.html', {"username": username, "first_name": first_name, "last_name": last_name})

def general(request):
    author = get_object_or_404(User, pk=1)
    memory = get_object_or_404(Memory, pk=1)
    username = author.username
    first_name = author.first_name
    last_name = author.last_name
    email = author.email
    users = User.objects.all()
    return render(request, 'general.html', {"username": username, "first_name": first_name, "last_name": last_name, "email": email})

def delete(request):
    author = get_object_or_404(User, pk=1)
    memory = get_object_or_404(Memory, pk=1)
    username = author.username
    return render(request, 'delete.html', {"username": username})