# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _, ugettext as __
from ragendja.auth.models import UserTraits
from django.forms.util import ErrorList

from sodo.models import List

# List forms
class ListCreateForm(forms.ModelForm):
	
	parent_list = forms.ModelChoiceField(required=False, queryset=List.all())
	
	class Meta:
		model = List
		fields = ('name',)
		


# User Forms
class UserLoginForm(forms.ModelForm):

	password = forms.CharField(widget=forms.PasswordInput(render_value=False),
		label=_(u'Password'))	

	class Meta:
		model = User
		fields = ('username',)


class UserProfileForm(forms.ModelForm):
	profile_image = forms.FileField(required=False, label=_("Upload a photo"))
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email')
		


class UserRegistrationForm(forms.ModelForm):
	
	password1 = forms.CharField(widget=forms.PasswordInput(render_value=False),
		label=_(u'Password'))
	password2 = forms.CharField(widget=forms.PasswordInput(render_value=False),
		label=_(u'Password (again)'))

	def clean_username(self):
		"""
		Validate that the username is alphanumeric and is not already
		in use.
		
		"""
		user = User.get_by_key_name("key_"+self.cleaned_data['username'].lower())
		if user and user.is_active:
		    raise forms.ValidationError(__(u'This username is already taken. Please choose another.'))
		return self.cleaned_data['username']

	def clean_email(self):
	    """
	    Validate that the supplied email address is unique for the
	    site.
	    
	    """
	    email = self.cleaned_data['email'].lower()
	    if User.all().filter('email =', email).filter(
				'is_active =', True).count(1):
			raise forms.ValidationError(__(u'This email address is already in use. Please supply a different email address.'))
	    return email
	
	def clean(self):
		"""
		Verifiy that the values entered into the two password fields
		match. Note that an error here will end up in
		``non_field_errors()`` because it doesn't apply to a single
		field.
		
		"""
		if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
			if self.cleaned_data['password1'] != self.cleaned_data['password2']:
				password_error = __(u'You must type the same password each time')
				self._errors['password1'] = ErrorList([password_error])

		return self.cleaned_data

    
	def save(self):
		cd = self.cleaned_data
		#if cd['password1'] == cd['password2']:
		user = super(UserRegistrationForm, self).save()
		user.set_password(cd['password1'])
			
		self.instance = user
		return user

    	
	class Meta:
		model = User
		fields = ('username', 'email')
