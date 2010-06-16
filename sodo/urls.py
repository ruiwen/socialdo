# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from sodo.views import *

urlpatterns = patterns('',

	url(r'^$', index, name='sodo.index'),
	
	# List methods
	url(r'list/(?P<index>\d+)/?$', list_show, name="sodo.list.show"),
	url(r'list/new/?$', list_new, name="sodo.list.new"),
	url(r'list/(?P<list_index>\d+)/new/item/?$', list_item_new, name="sodo.list.item.new"),
	url(r'list/collaborators/add/?', list_add_collaborator, name="sodo.list.collaborator.add"),

	# Item method
	url(r'item/new/?$', item_new, name="sodo.item.new"),
	url(r'item/(?P<item_id>\d+)/(?P<status>(in)?complete)/?', item_status_update, name="sodo.item.status.update"),
	url(r'item/(?P<item_id>\d+)/assign/?', item_assign, name="sodo.item.assign"),

	# User methods
	url(r'user/(?P<username>\w+)/?$', user_profile, name="sodo.user.show"),
	url(r'user/(?P<username>\w+)/add/friend/?$', user_add_friend, name="sodo.user.add.friend"),

	url(r'register/$', user_register, name='sodo.user.register'),
	#url(r'login/$', user_login, name='sodo.user.login'),
	#url(r'logout/$', user_logout, name='sodo.user.logout'),
	url(r'login/$', 'django.contrib.auth.views.login', {'template_name' : 'user/login.html'}),
	url(r'logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
	
	url(r'debug/$', debug, name='sodo.debug'),

)
