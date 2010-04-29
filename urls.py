# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

#handler500 = 'ragendja.views.server_error'

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    
    # Social do
    (r'', include('sodo.urls')),
    
    #(r'^$', 'django.views.generic.simple.direct_to_template',
    #    {'template': 'main.html'}),
    # Override the default registration form
    #url(r'^account/register/$', 'registration.views.register',
    #    kwargs={'form_class': UserRegistrationForm},
    #    name='registration_register'),
)

# Serve static files in DEBUG = TRUE environment
if settings.DEBUG:
    urlpatterns = urlpatterns + patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/ruiwen/Projects/SvarmDo/svarmdo/media/', 'show_indexes': True}),
    )
