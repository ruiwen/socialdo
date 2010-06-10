# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.utils.translation import ugettext as _
#from ragendja.template import render_to_response
from django.shortcuts import *
from utils import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q

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
	
	if request.user.is_authenticated():
		items = request.user.items.order_by('date_added')
		items_completed = request.user.items.filter(completed=True).count()
		items_incomplete = request.user.items.filter(completed=False).count()
		
		# Make sure we don't divide by 0
		if items_completed > 0:
			items_progress = int(( float(items_completed) / float(items_incomplete) ) * 100)
		else:
			items_progress = 0
			
		return render_to_response(request, 'index.html', {'lists':lists, 'items_progress':items_progress})

	else:
		return render_to_response(request, 'index.html', {'lists':lists})

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
		nitem = Item(user=request.user, primary_list=l, desc=request.POST['item-desc'])
		nitem.save()
		
	return HttpResponseRedirect(reverse('sodo.list.show', args=(int(list_index),)))
	
	

def list_show(request, index):
	
	# Retrieve list
	the_list = List.objects.get(id=int(index))
	return render_to_response(request, 'list/show.html', {'thelist':the_list})
	


def list_add_collaborator(request):
	
	if request.method == 'POST':
		
		try:
			l = List.objects.get(id=request.POST['list-id'])
			
			# Hunt for the user specified
			u = User.objects.get(Q(username=request.POST['user-value']) | Q(email=request.POST['user-value']))
			
			if u is not None:
				l.collaborators.add(u)
				messages.success(request, _("Collaboration request sent!"))
			
		except User.DoesNotExist:
			messages.error(request, _("User not found =("))
			
		except Exception:
			messages.error(request, _("Unable to send collaboration request"))
		
		return HttpResponseRedirect(request.META['HTTP_REFERER'])
		
	else:
		return HttpResponseForbidden()


def item_new(request):
	if request.method == 'POST':
		
		try:
			i = Item(user=request.user, desc=request.POST['item_name'], primary_list=List.objects.get(id=request.POST['list-tag']))
			i.save()
			
			messages.success(request, _("Item added successfully"))
		
		except Exception:
			messages.error(request, _("Whoops. Failed to create new item"))	
		
		
		return HttpResponseRedirect(request.META['HTTP_REFERER'])		
		
	else:	
		return HttpResponseRedirect(request.META['HTTP_REFERER'])	
		
	
		
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
			
			# Create the default list for this new User
			l = List(owner=user, name=user.username.capitalize(), desc=_("Default list for %(username)s" % {'username':user.username}))
			l.save()		
			
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
	
