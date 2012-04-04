"""
WSGI config for Oik project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""

import os, sys
sys.path.append('')
sys.path.append('/home/ec2-user/OIR/')

apache_configuration= os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace) 

#Add the path to 3rd party django application and to django itself.
sys.path.append('/home/ec2-user/Django-1.3.1/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'Oik.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
