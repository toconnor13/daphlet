# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from polls.models import Choice, Poll
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils import timezone



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
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('poll_results', args=(p.id,)))

def submit(request):
	question = request.POST['question']
	choice_1 = request.POST['choice_1']
	choice_2 = request.POST['choice_2']
	choice_3 = request.POST['choice_3']
	p = Poll(question=question, pub_date=timezone.now())
	p.save()
	p.choice_set.create(choice=choice_1, votes=0)
	p.choice_set.create(choice=choice_2, votes=0)
	p.choice_set.create(choice=choice_3, votes=0)
	p.save()
	return HttpResponse("You have successfully created a poll.")


@login_required
def test_session(request):
	return HttpResponse("Congratulations, you can access this user-restricted material.")

def stylesheet(request):
	return redirect('http://www.twitter.github.com/bootstrap/assets/css/bootstrap.css')

