from django.contrib import auth
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required

def index(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/student/dashboard")
	else:
		return render_to_response('index.html', RequestContext(request))