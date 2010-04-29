import os
import sys

sys.path.append('/home/ruiwen/Projects/SvarmDo/django-trunk')
sys.path.append('/home/ruiwen/Projects/SvarmDo/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'svarmdo.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()