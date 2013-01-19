from django.conf.urls import patterns, include, url

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
    url(r'^polls/', include('polls.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'auth_views.login'),
    url(r'^accounts/register/$', 'accounts.views.register'),
    url('^accounts/passwordreset', 'auth_views.password_reset'),
    url('^acounts/password_reset_done','django.contrib.auth.views.password_reset_done'),
    url(r'^stylesheet/$', 'polls.views.stylesheet'),
    
)
