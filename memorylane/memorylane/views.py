from django.shortcuts import get_object_or_404, render
from django.template import Template, Context
from django.http import HttpResponse
from .forms import *
from datetime import datetime
from .models import User, Memory

from django.contrib.auth import logout
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
	output = ', '.join([u.first_name for u in lastest_user_list])
	return HttpResponse(output)

def signup(request):
    register(request)
	
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=username,
            password=password,
            email=email
            )
            return HttpResponseRedirect('/signup/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form
    })
    return render(request, 'signup.html', {})

def settings(request):
	return render(request, 'settings.html', {})

def post(request, memory_id):
	memory = get_object_or_404(Memory, pk=memory_id)
	author = get_object_or_404(User, pk=memory.author)
	return render(request, 'post.html', {'memory': memory, 'author': author, 'image' : memory.image.name[10:]})

def newpost(request):
    author = get_object_or_404(User, pk=1)
    username = author.username
    return render(request, 'newpost.html', {"username": username})

def newpostsubmit(request):
    if 'title' in request.POST:
        m = Memory(name=request.POST['title'], author=1, location=request.POST['location'], date_created=datetime.now(), description=request.POST['note_text'], image=request.FILES['media'])
        m.save()
        memory = get_object_or_404(Memory, pk=m.id)
        author = get_object_or_404(User, pk=memory.author)
        return post(request, m.id)
        message = 'Successfully added a new memory'
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)

def passwordreset(request):
	return render(request, 'password-reset.html', {})

def login(request):
    if request.method == 'POST':
        user = get_object_or_404(User, password=request.POST['password'], email=request.POST['email'])
        return timeline(request, user)
    return render(request, 'login.html', {})

def friends(request):
	return render(request, 'friends.html', {})

def following(request):
    return render(request, 'following.html', {})

def follower(request):
    return render(request, 'follower.html', {})

def register(request):
    if request.method == 'POST':
        users = User.objects.all()
        for x in users:
            if x.username==request.POST['username']:
                return HttpResponse('That username is taken, please choose another one.')
            if x.email==request.POST['email']:
                return HttpResponse('That email is already in use.')    
        user = User(username=request.POST['username'], password=request.POST['password'], email=request.POST['email'], date_created=datetime.now())
        user.save()
        return timeline(request, user)    
    else:
        return HttpResponseRedirect('/signup/')

#@login_required
def home(request):
    return render_to_response('home.html',{'user': request.user })

def timeline(request, currentuser):
    author = get_object_or_404(User, pk=1)
    memory = get_object_or_404(Memory, pk=1)
    username = author.username
    first_name = author.first_name
    description = memory.description
    location = memory.location
    name = memory.name
    image = memory.image
    date_created = memory.date_created
    users = User.objects.all()
    memories = Memory.objects.all()
    return render(request, 'timeline.html', {"memories": memories})

def timeline(request):
    author = get_object_or_404(User, pk=1)
    memory = get_object_or_404(Memory, pk=1)
    username = author.username
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
    author = get_object_or_404(User, pk=1)
    memory = get_object_or_404(Memory, pk=1)
    username = author.username
    first_name = author.first_name
    description = memory.description
    location = memory.location
    name = memory.name
    image = memory.image
    date_created = memory.date_created
    memories = Memory.objects.all()
    if request.method == 'POST':
        form = BioForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/Saved/')
    else:
        author = get_object_or_404(User, pk=1)
        bio = author.bio
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