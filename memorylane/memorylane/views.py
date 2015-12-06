from django.shortcuts import get_object_or_404, render
from django.template import Template, Context
from django.http import HttpResponse
from .forms import *
from datetime import datetime
from .models import Memory
from .models import UserProfile
from django.contrib.auth.models import User
from friendship.models import Friend, Follow

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as a_login
from django.contrib.auth import logout as a_logout
from django.contrib.auth.hashers import check_password

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

def profiletest(request, user_id):
    u = User.objects.get(pk=user_id)
    output = ("<h1>You're looking at user %s.</h1>" % request.user.username)
    profile = get_object_or_404(UserProfile, username=request.user.username).bio
    output = output + "<br>" + u.username + " " + u.last_name + " " + profile
    return HttpResponse(output)

def userlist(request):
	lastest_user_list = User.objects.order_by('pk')[:7]
	output = ', '.join([u.username+' '+u.email for u in lastest_user_list])
	return HttpResponse(output)

def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/timeline/')
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
                
                user = get_object_or_404(User, email=email)
                user = authenticate(username=user.username, password=password)
                if user is not None:
                    if user.is_active:
                        a_login(request, user)
                
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
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    memory = get_object_or_404(Memory, pk=memory_id)
    author = get_object_or_404(User, username=memory.author)
    l = memory.location
    memories = Memory.objects.all()
    all_friends = Friend.objects.friends(request.user)
    return render(request, 'post.html', {'memory': memory, 'author': author, 'image' : memory.image.name[10:], 'memories': memories, 'all_friends': all_friends})

def newpost(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    username = request.user.username
    return render(request, 'newpost.html', {"username": username})

def newpost_new(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    username = request.user.username
    return render(request, 'newpost_new.html', {"username": username})

def newpostsubmit(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
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

def search(request):
    location = request.GET[u'q']
    memories = Memory.objects.filter(location=location)
    return render(request, "location.html", {"memories": memories, "location": location})

def location(request, location):
    location = location.replace("+"," ")
    memories = Memory.objects.filter(location=location)
    return render(request, "location.html", {"memories": memories, "location": location})
  

def settingssubmit(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        if 'user_id' in request.POST:
            request.user.username = request.POST['username']
        elif 'email' in request.POST:
            request.user.email = request.POST['email']
        elif 'name' in request.POST:
            request.user.first_name=request.POST['name']
        request.user.save()  
    return HttpResponseRedirect('/account/')

def passwordreset(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    if request.user.is_authenticated() and request.method == 'POST':
        oldpass = request.POST['oldPassword']
        if check_password(oldpass, request.user.password):
            oldpasscheck = request.POST['oldPasswordCheck']
            newpass = request.POST['newPassword']
            if oldpass == oldpasscheck and oldpass != newpass:
                request.user.set_password(newpass)
                request.user.save()
                a_logout(request)
                return HttpResponseRedirect('/login/')
            else:
                return HttpResponseRedirect('/password-reset/')    
        else:
            return HttpResponseRedirect('/password-reset/')    
    return render(request, 'password-reset.html', {})

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/timeline/')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = get_object_or_404(User, email=email)
        user = authenticate(username=user.username, password=password)
        if user is not None:
            if user.is_active:
                a_login(request, user)
        else:
            return login(request)        
        return HttpResponseRedirect('/timeline/')
    
    return render(request, 'login.html', {})

def logout(request):
    a_logout(request)
    return HttpResponseRedirect('/login/')    

def friends(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
	return render(request, 'friends.html', {})

def following(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    return render(request, 'following.html', {})

def follower(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    return render(request, 'follower.html', {})

def timeline(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
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
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    author = get_object_or_404(UserProfile, username=request.user.username)
    memory = get_object_or_404(Memory, pk=1)
    username = request.user.username
    first_name = request.user.first_name
    last_name = request.user.last_name
    description = memory.description
    location = memory.location
    name = memory.name
    image = memory.image
    date_created = memory.date_created
    memories = Memory.objects.filter(author=request.user.username)
    if request.method == 'POST':
        bio = get_object_or_404(UserProfile, username=request.user.username).bio
        form = BioForm(request.POST)
        bio = form.bioTextArea
        if form.is_valid():
            return HttpResponseRedirect('/Saved/')

    else:
        author = request.user
        bio = get_object_or_404(UserProfile, username=request.user.username).bio
        return render(request, 'profile-mod.html', {"user": author, "bio": bio, "memories": memories, "first_name" : first_name, "username": username, "description": description, "name": name, "location": location, "image": image, "date_created": date_created})

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

def location(request, location):
    location = location.replace("+"," ")
    memories = Memory.objects.filter(location=location)
    return render(request, "location.html", {"memories": memories, "location": location})

def myprofile(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    profile = get_object_or_404(UserProfile, username=request.user.username)
    users = User.objects.all()
    memories = Memory.objects.filter(author=request.user.username)
    if request.method == 'POST':
        profile.bio = request.POST['newBio']
        profile.save()
    return render(request, 'settings/myprofile.html', {"memories": memories, "profile": profile, "user":request.user})

def account(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    author = request.user
    memory = get_object_or_404(Memory, pk=1)
    username = author.username
    first_name = author.first_name
    last_name = author.last_name
    users = User.objects.all()
    memories = Memory.objects.all()
    return render(request, 'settings/account.html', {"user": author})

def general(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    author = get_object_or_404(User, pk=1)
    memory = get_object_or_404(Memory, pk=1)
    username = author.username
    first_name = author.first_name
    last_name = author.last_name
    email = author.email
    users = User.objects.all()
    return render(request, 'settings/general.html', {"username": username, "first_name": first_name, "last_name": last_name, "email": email})

def delete(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    if request.user.is_authenticated() and request.method == 'POST':
        if check_password(request.POST['password'], request.user.password):
            request.user.delete()
            return HttpResponseRedirect('/logout/')   
    return render(request, 'settings/delete.html', {})