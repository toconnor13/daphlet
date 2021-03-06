from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from polls.models import Poll

urlpatterns = patterns('',
		url(r'^$','polls.views.index', name="homepage"), 
		url(r'^(?P<poll_id>\d+)/$','polls.views.detail'),
		url(r'^(?P<poll_id>\d+)/results/$','polls.views.results'),
		url(r'^(?P<poll_id>\d+)/vote/$','polls.views.vote'),
		url(r'^(?P<poll_id>\d+)/delete/$', 'polls.views.delete'),
		url(r'^create_poll/1/$', 'polls.views.create_poll1'),
		url(r'^create_poll/2/$', 'polls.views.create_poll2'),
		url(r'^poll_complete/$', 'polls.views.poll_complete'),
		url(r'^user/account/$', 'polls.views.account', name="my_polls"),
		url(r'^contact/', 'polls.views.contact', name="contact_page"),
		)
