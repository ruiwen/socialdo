# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from ragendja.template import render_to_response

# Models
from sodo.models import *

def index(request):
	
	# Get latest lists
	lists = List.all().order('date_modified')	
	return render_to_response(request, 'index.html', {'lists':lists})


def show_list(request, index):
	
	# Retrieve list
	the_list = List.get_by_id(int(index))
	return render_to_response(request, 'list.html', {'thelist':the_list})
	

def show_user(request, username):

	# Retrieve user
	user = User.all().filter("username =", username).get()
	return render_to_response(request, 'user.html', {'user':user})