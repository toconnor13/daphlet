from django.conf.urls import patterns, include, url
from emailusernames.forms import EmailAuthenticationForm
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'daphlet.views.home', name='home'),
    # url(r'^daphlet/', include('daphlet.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^','polls.views.index'),
	url(r'^$', RedirectView.as_view(url='polls')), 
    url(r'^polls/', include('polls.urls') ),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login', 
	    {'authentication_form': EmailAuthenticationForm}, name='login'),
#    url(r'^accounts/register/$', 'polls.views.register'),
	url(r'^passwordreset', 'django.contrib.auth.views.password_reset'),
	url(r'^password_reset_done','django.contrib.auth.views.password_reset_done'),
	url(r'^password_reset_confirm','django.contrib.auth.views.password_reset_confirm'),
	url(r'^logout','django.contrib.auth.views.logout'),
	url(r'accounts/', include('registration.backends.default.urls')),
    
)
