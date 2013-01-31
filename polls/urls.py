from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from polls.models import Poll

urlpatterns = patterns('',
		url(r'^$','polls.views.index'), 
		url(r'^(?P<poll_id>\d+)/$','polls.views.detail'),
	#		DetailView.as_view(
	#			model=Poll,
	#			template_name='polls/detail.html')),
		url(r'^(?P<poll_id>\d+)/results/$','polls.views.results'),
		url(r'^(?P<poll_id>\d+)/vote/$','polls.views.vote'),
		url(r'^create_poll/2/$', 'polls.views.create_poll'),
		url(r'^(?P<poll_id>\d+)/poll_complete/$', 'polls.views.poll_complete'),
		url(r'^create_poll/1/$', 'polls.views.create_poll1'),
		)
