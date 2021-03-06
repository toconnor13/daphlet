# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext, Context
from django.template.loader import get_template
from polls.models import Choice, Poll, PollForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.mail.message import EmailMessage
from django.utils import timezone
from django import forms
from emailusernames.forms import EmailAuthenticationForm, EmailAdminAuthenticationForm, EmailUserCreationForm, EmailUserChangeForm
import re
import os
import datetime

def index(request):
	latest_poll_list = sorted(Poll.objects.all(), key=Poll.vote_count, reverse=True)
	register_form = EmailUserCreationForm
	path = request.path
	return render_to_response('polls/index.html', {
		'latest_poll_list': latest_poll_list,
		'register_form': register_form,
		'path': path,
		}, context_instance=RequestContext(request))

def contact(request):
	path = request.path
	return render_to_response('polls/contact.html',{'path': path}, context_instance=RequestContext(request))

def account(request):
	user_poll_list = Poll.objects.filter(author=request.user.username)
	path = request.path
	return render_to_response('polls/account.html', {'user_poll_list': user_poll_list, 'path': path}, context_instance=RequestContext(request))


@login_required
def detail(request, poll_id):
	p = get_object_or_404(Poll, pk=poll_id)
	close_time = p.close_date
	if p.close_date < timezone.now():
		return render_to_response('polls/detail.html', {
			'poll': p,
			'error_message': "The poll has closed.",
			'closed': True,
			'close_time': p.close_date,
			}, context_instance=RequestContext(request))
	return render_to_response('polls/detail.html', {'poll': p,
			'close_time': close_time,}, context_instance=RequestContext(request))


@login_required
def results(request, poll_id):
	p = get_object_or_404(Poll, pk=poll_id)
	try:
		user_id_list = eval(p.has_voted_list)
	except:
		return render_to_response('polls/detail.html', {
			'poll': p,
			'error_message': "There are no votes to count, so no results to see!",
			}, context_instance=RequestContext(request))

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
	list_of_emails = p.restrict_to_emails
	if p.close_date < timezone.now():
			return render_to_response('polls/detail.html', {
					'poll': p,
					'error_message': "The poll has closed.",
					'closed': True,
					'close_time': p.close_date,
					}, context_instance=RequestContext(request))
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render_to_response('polls/detail.html', {
			'poll':p,
			'error_message': "You didn't select a choice.",
			}, context_instance=RequestContext(request))
	else:
		if p.restrict_to_domain == u'None' or re.search(p.restrict_to_domain, request.user.username) or request.user.username in list_of_emails:
			if p.has_voted_list == u'' or not request.user.id in eval(p.has_voted_list):
				selected_choice.votes += 1
				string_to_join = str(request.user.id)+','
				p.has_voted_list += string_to_join
				p.save()
				selected_choice.save()
				return HttpResponseRedirect(reverse('polls.views.results', args=(p.id,)))
			else:
				return render_to_response('polls/detail.html', {
					'poll':p,
					'error_message': "You have already voted in this poll.",
					}, context_instance=RequestContext(request)) 
					
		else:
			return render_to_response('polls/detail.html', {
				'poll': p,
				'error_message': 'You are not allowed to vote on the poll!',
				}, context_instance=RequestContext(request))


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
	restricted_by_domain = False
	restricted_by_list = False
	add_close_date = False
	if 'close_date' in request.POST:
		add_close_date= True
	if request.POST['restrict'] == 'restrict_choice':
		restricted_by_domain = True
	if request.POST['restrict'] == 'email_restrict':
		restricted_by_list = True
	i=0
	choicelist = []
	while i < int(no_of_choices):
		name = 'choice_' + str(i) 
		choicelist.append(name)
		i += 1
	return render_to_response("polls/create_poll2.html", {
		'question': question,
		'choicelist': choicelist,
		'restricted': restricted_by_domain,
		'restricted_by_list': restricted_by_list,
		'add_close_date': add_close_date,
		},
		context_instance=RequestContext(request)
		)


@login_required
def poll_complete(request):
	question = request.POST['question']
	p = Poll(question=question, pub_date=timezone.now())
	p.author = request.user.username
	raw_choicedict = request.POST.copy()
	if 'restricted_domain' in request.POST:
		p.restrict_to_domain = request.POST['restricted_domain']
		del raw_choicedict['restricted_domain']
	if 'email_list' in request.POST:
		p.restrict_to_emails = request.POST['email_list']
		p.restrict_to_emails = raw_choicedict['email_list'].split(',')
		p.restrict_to_domain = u'Invalid'
		del raw_choicedict['email_list']
	if 'close_time' in request.POST:
			time_string = raw_choicedict['close_time']
			time_pattern = r'(\d+)-(\d+)-(\d+)\s(\d+):(\d+)'
			match = re.search(time_pattern, time_string)
			given_date = datetime.datetime(int(match.group(1)), int(match.group(2)),int(match.group(3)), int(match.group(4)), int(match.group(5)))
			p.close_date = given_date
			del raw_choicedict['close_time']
	p.save()
	del raw_choicedict['csrfmiddlewaretoken']
	del raw_choicedict['question']
	choice_list = raw_choicedict.values()
	for option in choice_list:
		p.choice_set.create(choice=option, votes=0)
	p.save()


	poll_message = get_template('polls/poll_mail.txt')
	
	d = Context({ 'poll_id': p.id, 
			'SITE_URL': os.environ['SITE_URL'],
			})
	text_content = poll_message.render(d)
	msg = EmailMessage('New Poll Created', text_content, 'daphlet.polls@tcd.ie', [request.user.username])
	msg.send()

	return HttpResponseRedirect(reverse('polls.views.detail', args=(p.id,)))

def delete(request, poll_id):
	p = Poll.objects.get(id=poll_id)
	if p.author == request.user.username:
		message = 'You have deleted the poll " ' + p.question + ' ".'
		p.delete()
		user_poll_list = Poll.objects.filter(author=request.user.username)
		return render_to_response('polls/account.html', {'user_poll_list': user_poll_list, 'message':message,}, context_instance=RequestContext(request))
	
	else:
		return HttpResponse("You can't delete this.")
