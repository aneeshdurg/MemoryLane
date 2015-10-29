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
    # register(request)
	return render(request, 'signup.html', {})
    # if request.method == 'POST':
    #     form = RegistrationForm(request.POST)
    #     if form.is_valid():
    #         user = User.objects.create_user(
    #         username=username,
    #         password=password,
    #         email=email
    #         )
    #         return HttpResponseRedirect('/signup/success/')
    # else:
    #     form = RegistrationForm()
    # variables = RequestContext(request, {
    # 'form': form
    # })

def settings(request):
	return render(request, 'settings.html', {})

def post(request, memory_id):
	memory = get_object_or_404(Memory, pk=memory_id)
	author = get_object_or_404(User, pk=memory.author)
	return render(request, 'post.html', {'memory': memory, 'author': author, 'image' : memory.image.name[10:]})

def newpost(request):
    return render(request, 'newpost.html', {})

def newpostsubmit(request):
    if 'title' in request.POST:

        m = Memory(name=request.POST['title'], author=1, location="Siebel Center", date_created=datetime.now(), description=request.POST['note_text'], image=request.FILES['media'])
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
    # if request.method == 'POST':
    #     form = RegistrationForm(request.POST)
    #     if form.is_valid():
    #         user = User.objects.create_user(
    #         username=username,
    #         password=password,
    #         )
    #         return HttpResponseRedirect('/register/success/')
    # else:
    #     form = RegistrationForm()
    # variables = RequestContext(request, {
    # 'form': form
    # })
    # else
    return render(request, 'login.html', {})

def friends(request):
	return render(request, 'friends.html', {})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User(username=form.cleaned_data['username'], password=form.cleaned_data['password'], email=form.cleaned_data['email'], date_created=datetime.now())
            user.save()
            return HttpResponseRedirect('/timeline/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form
    })
 
    return timeline(request)
 
def register_success(request):
    return render_to_response(
    'registration/success.html',
    )
 
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')
 
#@login_required
def home(request):
    return render_to_response(
    'home.html',
    { 'user': request.user }
    )	
def timeline(request):
    return render(request, 'timeline.html', {})

def profilemod(request):
    return render(request, 'profile-mod.html', {})
