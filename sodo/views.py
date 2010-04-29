# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
#from ragendja.template import render_to_response
from django.shortcuts import *
from utils import render_to_response
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
	lists = List.objects.order_by('date_modified')	
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
			nlist.save()
		
			return HttpResponseRedirect(reverse('sodo.show.list', args=(nlist.id,)))					
		
		return render_to_response(request, 'list/new.html', {'lform':lform})			



def list_item_new(request, list_index):
	
	if request.method == 'POST':
		# Retrieve the list
		l = List.objects.get(id=int(list_index))
		nitem = Item(user=request.user, parent_list=l, desc=request.POST['item-desc'])
		nitem.save()
		
	return HttpResponseRedirect(reverse('sodo.show.list', args=(int(list_index),)))
	
	

def list_show(request, index):
	
	# Retrieve list
	the_list = List.objects.get(id=int(index))
	return render_to_response(request, 'list/show.html', {'thelist':the_list})
	
	

def user_add_friend(request, username):
	
	friend = User.objects.get(username=username)
	if request.user.is_authenticated():
		
		request.user.collaborators.add(friend.id)
		request.user.save()
		
		
#		if friend.first_name and friend.last_name:
#			name = friend.get_full_name()
#		else:
#			name = friend.username
		
		message = _('Collaboration request sent to %(name)s') % {'name': friend}
		
	else:
		message = _("Whoops")

	
	uform = UserProfileForm(instance=friend)
	
	
	return render_to_response(request, 'user/user.html', {'profileuser':friend, 'success':message, 'uform':uform})


def user_profile(request, username):

	if request.method == 'GET':
		# Retrieve user
		profileuser = User.objects.get(username__exact=username)
		
		uform = UserProfileForm(instance=profileuser);
		
		return render_to_response(request, 'user/user.html', {'profileuser':profileuser, 'uform':uform})

	elif request.method == 'POST':
		
		profileuser = User.objects.get(username__exact=username) # Retrieve the specified user
		uform = UserProfileForm(request.POST, instance=profileuser) # Populate the UserProfileForm with the input data from client side				

		if uform.is_valid():

			user = uform.save()									
			cd = uform.cleaned_data
			
#			# Process the data in form.cleaned_data
#			media = None
#			try:
#				media = Media()
#				tmp_img = db.Blob(request.FILES['profile_image'].read())
#				media.name = request.FILES['profile_image'].name
#				media.is_blob = True
#				media.blob_content = tmp_img
#				media.content_type = request.FILES['profile_image'].content_type
#				media.put()
#			except KeyError:
#				media = None
#
#			if media:
#				user.profile_image = media
#				user.put()
	
			
			message = {'text': _("Profile updated"), 'type':'success'}
		else:
			#uform = UserProfileForm(instance=user)
			message = {'text':_("Profile update failed"), 'type':'error'}		
			return render_to_response(request, 'user/user.html', {'uform':uform, 'profileuser':profileuser, 'message':message, 'errors':uform.errors })

		return render_to_response(request, 'user/user.html', {'uform':uform, 'profileuser':profileuser, 'message':message})

	
	
def user_register(request):

	if request.method == 'GET':
		uform = UserRegistrationForm()
		return render_to_response(request, 'user/register.html', {'uform':uform})
		
	elif request.method == 'POST':
		
		uform = UserRegistrationForm(request.POST)
		
		if uform.is_valid():
			user = uform.save()
						
			auser = authenticate(username=user.username, password=request.POST['password1'])
			if auser and auser.is_authenticated():
				login(request, auser)
				return HttpResponseRedirect('/')

		return render_to_response(request, 	'user/register.html', {'uform':uform})	


def user_login(request):
	
	if request.method == 'GET':
		uform = UserLoginForm()
		return render_to_response(request, 'user/login.html', {'uform':uform})
		
	elif request.method == 'POST':
		
		uform = UserLoginForm(request.POST)
		if uform.is_valid():
			cd = uform.cleaned_data
			user = authenticate(username=cd['username'], password=cd['password'])
			if user and user.is_authenticated():
				login(request, user)
				return HttpResponseRedirect(reverse('sodo.index'))
		
		return render_to_response(request, 'user/login.html', {'uform':uform})
	
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('sodo.index'))
	
