# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response 
from django.http import HttpResponseRedirect, HttpResponse 
from django.core.urlresolvers import reverse 
from django.template import RequestContext 
from polls.models import Choice, Poll 
from django.contrib.auth import authenticate, login 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 


def register(request):
	username = request.POST['username']
	password = request.POST['password']
	email = request.POST['email']
	user = User.objects.create_user(username,email,  password)
	user.save()
	return HttpResponse("You have successfully registered.")
