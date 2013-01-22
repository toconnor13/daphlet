# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response 
from django.http import HttpResponseRedirect, HttpResponse 
from django.core.urlresolvers import reverse 
from django.template import RequestContext 
from polls.models import Choice, Poll 
from django.contrib.auth import authenticate, login 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 
from django.conf import settings
from django import forms
from django.contrib.auth.forms import UserCreationForm


def register0(request):
	username = request.POST['username']
	password = request.POST['password']
	email = request.POST['email']
	user = User.objects.create_user(username,email,  password)
	user.save()
	return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)


def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			return HttpResponseRedirect("/polls/")
		else:
			form = UserCreationForm()
		return render_to_response("registration/register.html", {
			'form': form,
			})

