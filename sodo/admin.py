from django.contrib import admin
from django.contrib.auth.models import User
from sodo.models import List, Item, Media

admin.site.unregister(User)
admin.site.register(User)
admin.site.register(Media)
admin.site.register(List)
admin.site.register(Item)
