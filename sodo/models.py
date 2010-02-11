# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from google.appengine.ext import db
from ragendja.auth.models import User

                
class Media(db.Model):
	name = db.StringProperty()
	string_content = db.StringProperty()
	is_blob = db.BooleanProperty()
	blob_content = db.BlobProperty()
	content_type = db.StringProperty()
        
class User(User):	
	profile_image = db.ReferenceProperty(Media, collection_name="user_images", required=False)
	

class List(db.Model):
	parent_list = db.SelfReferenceProperty(default=None)
	user = db.ReferenceProperty(User, required=True, collection_name="lists")
	date_added = db.DateTimeProperty(auto_now_add=True)
	date_modified = db.DateTimeProperty(auto_now=True)
	name = db.StringProperty()

	
class Item(db.Model):
	completed = db.BooleanProperty(default=False)
	user = db.ReferenceProperty(User)
	desc = db.StringProperty(multiline=True)
	parent_list = db.ReferenceProperty(List, collection_name="list_items")
	date_added = db.DateTimeProperty(auto_now_add=True)
	date_modified = db.DateTimeProperty(auto_now=True)
	date_completed = db.DateTimeProperty()
	completed_by = db.ReferenceProperty(User, collection_name='completed_items')
	
	
	