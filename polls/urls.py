from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from polls.models import Poll

urlpatterns = patterns('',
		url(r'^$', 
			ListView.as_view(
				queryset = sorted(Poll.objects.all(), key=Poll.vote_count, reverse=True),
				context_object_name='latest_poll_list',
				template_name='polls/index.html')),
		url(r'^(?P<pk>\d+)/$',
			DetailView.as_view(
				model=Poll,
				template_name='polls/detail.html')),
		url(r'^(?P<pk>\d+)/results/$',
			DetailView.as_view(
				model=Poll,
				template_name='polls/results.html'),
			name='poll_results'),
		url(r'^(?P<poll_id>\d+)/vote/$','polls.views.vote'),
		url(r'^test/$', 'polls.views.test_session'),
		url(r'^submit/$', 'polls.views.submit'),
		url(r'^style.css', 'polls.views.stylesheet'),
		#url(r'^style.css', 'direct_to_template', {'template': 'style.css'}),

		)
