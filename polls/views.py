# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from polls.models import Choice, Poll, PollForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils import timezone
from django import forms
from emailusernames.forms import EmailAuthenticationForm, EmailAdminAuthenticationForm, EmailUserCreationForm, EmailUserChangeForm
import re


def index(request):
	latest_poll_list = sorted(Poll.objects.all(), key=Poll.vote_count, reverse=True)
	register_form = EmailUserCreationForm
	return render_to_response('polls/index.html', {
		'latest_poll_list': latest_poll_list,
		'register_form': register_form,
		}, context_instance=RequestContext(request))

def contact(request):
	return render_to_response('polls/contact.html', context_instance=RequestContext(request))

def account(request):
	user_poll_list = Poll.objects.filter(author=request.user.username)
	return render_to_response('polls/account.html', {'user_poll_list': user_poll_list,}, context_instance=RequestContext(request))


@login_required
def detail(request, poll_id):
	p = get_object_or_404(Poll, pk=poll_id)
	return render_to_response('polls/detail.html', {'poll': p,}, context_instance=RequestContext(request))


@login_required
def results(request, poll_id):
	p = get_object_or_404(Poll, pk=poll_id)
	user_id_list = eval(p.has_voted_list)
	username_list = []
	for i in user_id_list:
		username_list.append(User.objects.get(id=i))
	return render_to_response('polls/results.html', {
		'poll': p,
		'users': username_list,
		}, context_instance=RequestContext(request))

@login_required
def vote(request, poll_id):
	p = get_object_or_404(Poll, pk=poll_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render_to_response('polls/detail.html', {
			'poll':p,
			'error_message': "You didn't select a choice.",
			}, context_instance=RequestContext(request))
	else:
		if p.restrict_to_domain == u'None' or re.search(p.restrict_to_domain, request.user.username):
#			except KeyError:
#				pass
			if p.has_voted_list == u'' or not request.user.id in eval(p.has_voted_list):
				selected_choice.votes += 1
				string_to_join = str(request.user.id)+','
				p.has_voted_list += string_to_join
				p.save()
				selected_choice.save()
				return HttpResponseRedirect(reverse('polls.views.results', args=(p.id,)))
			else:
				return HttpResponse('It seems you have already voted.')
		else:
			return HttpResponse('You are not allowed to vote on this poll.')


def register(request):
	if request.method == 'POST':
		form = EmailUserCreationForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			return HttpResponseRedirect("/polls/")
	else:
		form = UserCreationForm()
	return render_to_response("registration/register.html", {
		'form': form,},
		context_instance=RequestContext(request)
		)


@login_required
def create_poll1(request):
	return render_to_response('polls/create_poll1.html', context_instance=RequestContext(request))

@login_required
def create_poll2(request):
	question=request.POST['question']
	no_of_choices = request.POST['no_of_choices']
	restricted = False
	if 'restrict_choice' in request.POST:
		restricted = True
	i=0
	choicelist = []
	while i < int(no_of_choices):
		name = 'choice_' + str(i) 
		choicelist.append(name)
		i += 1
	return render_to_response("polls/create_poll2.html", {
		'question': question,
		'choicelist': choicelist,
		'restricted': restricted,},
		context_instance=RequestContext(request)
		)


@login_required
def poll_complete(request):
	question = request.POST['question']
	p = Poll(question=question, pub_date=timezone.now())
	p.author = request.user.username
	if 'restricted_domain' in request.POST:
		p.restrict_to_domain = request.POST['restricted_domain']
	p.save()
	raw_choicedict = request.POST.copy()
	del raw_choicedict['csrfmiddlewaretoken']
	del raw_choicedict['question']
	if 'restricted_domain' in raw_choicedict:
		del raw_choicedict['restricted_domain']
	choice_list = raw_choicedict.values()
	for option in choice_list:
		p.choice_set.create(choice=option, votes=0)
	p.save()

	message = "You have just created a new poll on Daphlet."
	send_mail('New poll created', message, 'daphlet.polls@gmail.com', [request.user.username], fail_silently=False)
	return HttpResponseRedirect(reverse('polls.views.detail', args=(p.id,)))

def delete(request, poll_id):
	p = Poll.objects.get(id=poll_id)
	if p.author == request.user.username:
		p.delete()
		return HttpResponse("it's gone.")
	else:
		return HttpResponse("you can't delete this.")
