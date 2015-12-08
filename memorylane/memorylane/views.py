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

import googlemaps

def profiletest(request, user_id):
    u = User.objects.get(pk=user_id)
    output = ("<h1>You're looking at user %s.</h1>" % request.user.username)
    profile = get_object_or_404(UserProfile, username=request.user.username).bio
    output = output + "<br>" + u.username + " " + u.last_name + " " + profile
    return HttpResponse(output)

def userlist(request):
	lastest_user_list = User.objects.order_by('pk')[:11]
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
            fname = request.POST['fname']
            lname = request.POST['lname']
            if form.is_valid():
                user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=fname,
                last_name=lname
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
    authorProfile = get_object_or_404(UserProfile, username=memory.author)
    location = memory.location
    gmaps = googlemaps.Client(key="AIzaSyCdgUowprALYpEowr3eIYlKq_8M0ldb6-I")
    geocode_result = gmaps.geocode(location)
    lat = geocode_result[0]['geometry']['bounds']['northeast']['lat']
    lng = geocode_result[0]['geometry']['bounds']['northeast']['lng']
    memories = Memory.objects.filter(lat=lat).filter(lng=lng)
    authorProfileImages=[]
    for m in memories:
        authorProfile = get_object_or_404(UserProfile, username=m.author)
        authorProfileImages.append(authorProfile.image)
    link=zip(memories, authorProfileImages)
    all_friends = Friend.objects.friends(request.user)
    return render(request, 'post.html', {'memory': memory, 'author': author, 'authorProfile': authorProfile, 'image' : memory.image.name[10:], 'memories': memories, 'all_friends': all_friends, 'link': link})

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
        location=request.POST['location']
        gmaps = googlemaps.Client(key="AIzaSyCdgUowprALYpEowr3eIYlKq_8M0ldb6-I")
        geocode_result = gmaps.geocode(location)
        lat = geocode_result[0]['geometry']['bounds']['northeast']['lat']
        lng = geocode_result[0]['geometry']['bounds']['northeast']['lng']
        profile = get_object_or_404(UserProfile, username=request.user.username)
        m = Memory(name=request.POST['title'], author=request.user.username, first_name=request.user.first_name, last_name=request.user.last_name, location=request.POST['location'], lat=lat, lng=lng, date_created=datetime.now(), description=request.POST['note_text'], image=request.FILES['media'], author_image=profile.image)
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
    gmaps = googlemaps.Client(key="AIzaSyCdgUowprALYpEowr3eIYlKq_8M0ldb6-I")
    geocode_result = gmaps.geocode(location)
    lat = geocode_result[0]['geometry']['bounds']['northeast']['lat']
    lng = geocode_result[0]['geometry']['bounds']['northeast']['lng']
    memories = Memory.objects.filter(lat=lat).filter(lng=lng)
    return render(request, "location.html", {"memories": memories, "location": location})

def location(request, location):
    location = location.replace("+"," ")
    gmaps = googlemaps.Client(key="AIzaSyCdgUowprALYpEowr3eIYlKq_8M0ldb6-I")
    geocode_result = gmaps.geocode(location)
    lat = geocode_result[0]['geometry']['bounds']['northeast']['lat']
    lng = geocode_result[0]['geometry']['bounds']['northeast']['lng']
    memories = Memory.objects.filter(lat=lat).filter(lng=lng)
    return render(request, "location.html", {"memories": memories, "location": location, "lat": lat, "lng": lng})

def settingssubmit(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        if 'livesin' in request.POST:
            profile = get_object_or_404(UserProfile, username=request.user.username)
            profile.image = request.FILES['media']
            profile.livesin = request.POST['livesin']
            request.user.username = request.POST['username']
            request.user.email = request.POST['email']
            request.user.first_name=request.POST['fname']
            request.user.last_name=request.POST['lname']    
            profile.bio = request.POST['bio']
            profile.save()    
            request.user.save()  
        return HttpResponseRedirect('/profile-mod/')
    else:
        message = 'Please enter the location'
    return HttpResponse(message), HttpResponseRedirect('/account/')


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
    user = request.user
    memories = Memory.objects.all()
    authorProfileImages=[]
    for memory in memories:
        authorProfile = get_object_or_404(UserProfile, username=memory.author)
        authorProfileImages.append(authorProfile.image)
    link=zip(memories, authorProfileImages)
    return render(request, 'timeline.html', {"memories": memories, "user": user, "link": link})

def profilemod(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    author = get_object_or_404(UserProfile, username=request.user.username)
    username = request.user.username
    first_name = request.user.first_name
    last_name = request.user.last_name
    memories = Memory.objects.filter(author=request.user.username)
    user = request.user
    profile = get_object_or_404(UserProfile, username=request.user.username)
    return render(request, 'profile-mod.html', {"user": user, "memories": memories, "profile": profile })

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

def myprofile(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    profile = get_object_or_404(UserProfile, username=request.user.username)
    users = User.objects.all()
    memories = Memory.objects.filter(author=request.user.username)
    return render(request, 'settings/myprofile.html', {"memories": memories, "profile": profile, "user":request.user})

def account(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    user = request.user
    profile = get_object_or_404(UserProfile, username=request.user.username)
    return render(request, 'settings/account.html', {"user": user, "profile": profile})

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
            for m in Memory.objects.all():
                if m.author == request.user.username:
                    m.delete()
            for p in UserProfile.objects.all():
                if p.username == request.user.username:
                    p.delete()        
            request.user.delete()
            return HttpResponseRedirect('/logout/')   
    return render(request, 'settings/delete.html', {})

def imageUpload(request):
    form = PhotoForm(request.POST, request.FILES)
    if request.method=='POST':
        if form.is_valid():
            image = request.FILES['photo']
            new_image = Photo(photo=image)
            new_image.save()
            response_data=[{"success": "1"}]
            return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
    return render(request, 'imageUpload.html', {})