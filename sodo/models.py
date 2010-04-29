# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
import os
         
def get_image_path(instance, filename):
	return os.path.join('users', instance.id, filename) 
               
#class Media(models.Model):
#	name = models.CharField()
#	string_content = models.CharField()
#	is_blob = models.BooleanField()
#	blob_content = CustomImageField(upload_to=get_image_path)
#	content_type = models.CharField()
        

class UserProfile(models.Model):	
	user = models.ForeignKey(User, unique=True)
	profile_image = models.ImageField(upload_to=get_image_path, blank=True)
	collaborators = models.ManyToManyField("self", symmetrical=False)
	

class List(models.Model):
	parent_list = models.ForeignKey('List', blank=True, null=True, related_name="sub_lists")
	user = models.ForeignKey(User, related_name="lists")
	date_added = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	name = models.CharField(max_length=255, blank=False)
	
	def __str__(self):
		return self.name
		
	def __unicode__(self):
		return self.name

	
class Item(models.Model):
	completed = models.BooleanField(default=False)
	user = models.ForeignKey(User, related_name="items")
	desc = models.CharField(max_length=255)
	parent_list = models.ForeignKey(List, related_name="list_items")
	date_added = models.DateField(auto_now_add=True)
	date_modified = models.DateField(auto_now=True)
	date_completed = models.DateTimeField(null=True, blank=True)
	completed_by = models.ForeignKey(User, related_name='completed_items', blank=True, null=True)
	
	def __unicode__(self):
		return self.desc
	
	