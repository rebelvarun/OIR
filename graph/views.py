from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login


def index(request):
    if request.user.is_authenticated:
       #login(request, request.user)
       return render_to_response('admin/analytics.html',context_instance=RequestContext(request))
    else:
       return render_to_response('admin/login.html',context_instance=RequestContext(request))


