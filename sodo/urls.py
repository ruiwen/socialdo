# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from sodo.views import *

urlpatterns = patterns('',

	url(r'^$', index, name='sodo.index'),
	url(r'list/(?P<index>\d+)/?$', show_list, name="sodo.show.list"),
	url(r'user/(?P<username>\w+)/?$', show_user, name="sodo.show.user"),

	url(r'register/$', user_register, name='sodo.user.register'),
	url(r'login/$', user_login, name='sodo.user.login'),
	url(r'logout/$', user_logout, name='sodo.user.logout'),
	
	url(r'debug/$', debug, name='sodo.debug'),

)