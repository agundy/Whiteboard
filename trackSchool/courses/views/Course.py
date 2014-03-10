from django.contrib import auth
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from courses.forms import CourseForm

def create_course(request):
	"""
	form for creating a new course
	"""
	if request.method == 'POST':
		data = {'title': request.POST['title'],
				 'dept': request.POST['dept'],
				 'courseID': request.POST['courseID'],
				 'course_unique': request.POST['course_unique']}

		course_form = CourseForm(data)

		