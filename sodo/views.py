# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from ragendja.template import render_to_response
from django.contrib.auth import authenticate, login, logout

# Models
from sodo.models import *

# Forms
from sodo.forms import UserRegistrationForm

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


def show_list(request, index):
	
	# Retrieve list
	the_list = List.get_by_id(int(index))
	return render_to_response(request, 'list.html', {'thelist':the_list})
	

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
		else:
			return render_to_response(request, 'register.html', {'uform':uform})	
		
	