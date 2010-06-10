# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User, UserManager
import os
from itertools import chain
         
def get_image_path(instance, filename):
	return os.path.join('users', instance.id, filename) 
               
#class Media(models.Model):
#	name = models.CharField()
#	string_content = models.CharField()
#	is_blob = models.BooleanField()
#	blob_content = CustomImageField(upload_to=get_image_path)
#	content_type = models.CharField()
        

#class UserProfile(models.Model):	
#	user = models.ForeignKey(User, unique=True)
#	profile_image = models.ImageField(upload_to=get_image_path, blank=True)
#	collaborators = models.ManyToManyField("self", symmetrical=False)

class User(User):
	"""Custom User model, extending Django's default User"""
	profile_image = models.ImageField(upload_to=get_image_path, blank=True)
	contacts = models.ManyToManyField("self", symmetrical=False, blank=True)
	
	objects = UserManager()
	
	def lists(self, with_shared=True):
		if with_shared:
			#return self.owned_lists.all() + self.shared_lists.all()
			# TODO: lists() should return lists in order of last used
			return list(chain(self.owned_lists.all(), self.shared_lists.all()))
		else:
			return self.owned_lists.all()

	def items(self, with_assigned=True):
		if with_assigned:
			return list(chain(self.owned_items.all(), self.assigned_items.all()))
		else:
			return self.owned_items.all()

		
	def __unicode__(self):
		if self.first_name and self.last_name:
			return self.get_full_name()
		else:
			return self.username
	
	

class List(models.Model):
	parent_list = models.ForeignKey('List', blank=True, null=True, related_name="sub_lists")
	owner = models.ForeignKey(User, related_name="owned_lists")
	date_added = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	name = models.CharField(max_length=255, blank=False)
	desc = models.CharField(max_length=1024, blank=True, null=True)
	collaborators = models.ManyToManyField(User, related_name="shared_lists", blank=True)	
	
	
	def items_completed(self, with_secondary=True):
		completed = self.primary_items.filter(completed=True)
		
		if with_secondary:
			completed += self.secondary_items.filter(completed=True)
			
		return completed
	
	
	def items_incomplete(self, with_secondary=True):
		incomplete = self.primary_items.filter(completed=False)
		
		if with_secondary:
			incomplete += self.secondary_items.filter(completed=False)
			
		return incomplete
	
	
	def overall_progress(self, with_secondary=True):
		completed = self.items_completed(with_secondary)

		total = self.primary_items.all()
		if with_secondary:
			total += self.secondary_items.all()
		
		return int( (float(completed.count()) / float(total.count())) * 100 )
	
	
	def accept(self, item):
		self.secondary_items.add(item.id)
	
	def __str__(self):
		return self.name
		
	def __unicode__(self):
		return self.name

	
class Item(models.Model):
	completed = models.BooleanField(default=False)
	owner = models.ForeignKey(User, related_name="owned_items")
	assignee = models.ForeignKey(User, related_name="assigned_items") 
	desc = models.CharField(max_length=255)
	primary_list = models.ForeignKey(List, related_name="primary_items")
	secondary_lists = models.ManyToManyField(List, related_name="secondary_items", blank=True)
	date_added = models.DateField(auto_now_add=True)
	date_modified = models.DateField(auto_now=True)
	date_completed = models.DateTimeField(null=True, blank=True)
	completed_by = models.ForeignKey(User, related_name='completed_items', blank=True, null=True)
	
	def __unicode__(self):
		return self.desc
	
	