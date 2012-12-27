from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from polls.models import Choice, Poll
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def login(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:
			# Redirect to a success page
			return HttpResponse("You have successfully logged in.")
		else:
			# Redirect to a 'disabled account' page.
			return HttpResponse("Your account is disabled.")
	else:
		# Return an 'invalid login' error message.
		return HttpResponse("Your login details are invalid.")

