from django.contrib import admin
from django.contrib.auth.models import User

admin.site.unregister(User) # Deregister the built-in User model

from sodo.models import  User, List, Item # Import our own models
admin.site.register(User) # Register our own User model instead
admin.site.register(List)
admin.site.register(Item)
