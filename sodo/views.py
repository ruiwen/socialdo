# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from ragendja.template import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout

# Models
from sodo.models import *

# Forms
from sodo.forms import *
#from sodo.forms import ListCreateForm, UserRegistrationForm, UserLoginForm

def debug(request):
	# Misc
	session = request.session

	# Basic PartyBlank User stuff
	#user = None
	#if request.user.is_authenticated():
	user = request.user
	return render_to_response(request, 'debug.html', {'session':session,'user':user})


def index(request):
	
	# Get latest lists
	lists = List.all().order('date_modified')	
	return render_to_response(request, 'index.html', {'lists':lists, 'user':request.user})


def list_new(request):

	if request.method == 'GET':
		lform = ListCreateForm()
		return render_to_response(request, 'list/new.html', {'lform':lform})

	elif request.method == 'POST':
		lform = ListCreateForm(request.POST)
		
		if lform.is_valid():
			cd = lform.cleaned_data
			
			nlist = List(name=cd['name'], parent_list=cd['parent_list'], user=request.user)			
			nlist.put()
		
			return HttpResponseRedirect(reverse('sodo.show.list', args=(nlist.key().id(),)))					
		
		return render_to_response(request, 'list/new.html', {'lform':lform})			



def list_item_new(request, list_index):
	
	if request.method == 'POST':
		# Retrieve the list
		l = List.get_by_id(int(list_index))
		nitem = Item(user=request.user, parent_list=l, desc=request.POST['item-desc'])
		nitem.put()
		
	return HttpResponseRedirect(reverse('sodo.show.list', args=(int(list_index),)))
	
	

def list_show(request, index):
	
	# Retrieve list
	the_list = List.get_by_id(int(index))
	return render_to_response(request, 'list/show.html', {'thelist':the_list})
	
	

def show_user(request, username):

	# Retrieve user
	user = User.all().filter("username =", username).get()
	return render_to_response(request, 'user.html', {'user':user})
	
	
def user_register(request):

	if request.method == 'GET':
		uform = UserRegistrationForm()
		return render_to_response(request, 'register.html', {'uform':uform})
		
	elif request.method == 'POST':
		
		uform = UserRegistrationForm(request.POST)
		
		if uform.is_valid():
			user = uform.save()
			user.put()
			
			auser = authenticate(username=user.username, password=request.POST['password1'])
			if auser and auser.is_authenticated():
				login(request, auser)
				return HttpResponseRedirect('/')

		return render_to_response(request, 'register.html', {'uform':uform})	


def user_login(request):
	
	if request.method == 'GET':
		uform = UserLoginForm()
		return render_to_response(request, 'login.html', {'uform':uform})
		
	elif request.method == 'POST':
		
		uform = UserLoginForm(request.POST)
		if uform.is_valid():
			cd = uform.cleaned_data
			user = authenticate(username=cd['username'], password=cd['password'])
			if user and user.is_authenticated():
				login(request, user)
				return HttpResponseRedirect(reverse('sodo.index'))
		
		return render_to_response(request, 'login.html', {'uform':uform})
	
def user_logout(request):
	logout(request)
	return render_to_response(reverse('sodo.index'))
	
