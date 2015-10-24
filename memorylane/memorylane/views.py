from django.shortcuts import get_object_or_404, render
from django.template import Template, Context
from django.http import HttpResponse
from .forms import *

from .models import User, Memory


from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
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
	return render(request, 'signup.html', {})

def settings(request):
	return render(request, 'settings.html', {})

def post(request, memory_id):
	memory = get_object_or_404(Memory, pk=memory_id)
	author = get_object_or_404(User, pk=memory.author)
	return render(request, 'post.html', {'memory': memory, 'author': author})

def passwordreset(request):
	return render(request, 'password-reset.html', {})

def login(request):
	return render(request, 'login.html', {})

def friends(request):
	return render(request, 'friends.html', {})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form
    })
 
    return render_to_response(
    'registration/register.html',
    variables,
    )
 
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