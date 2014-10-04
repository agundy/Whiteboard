from django.contrib import auth
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from courses.forms import StudentForm


def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/student/dashboard")
    else:
        form = StudentForm()

        return render_to_response('index.html', {'form': form}, RequestContext(request))
