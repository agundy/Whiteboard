from django.conf.urls import patterns, include, url
from courses.views import *
from django.views.generic import TemplateView

urlpatterns = patterns('',

    # Student
    url(r'^student/create', Student.create_student),
    url(r'^student/login', Student.login),

    url(r'^group/profile', TemplateView.as_view(template_name='Group/profile.html')),

    url(r'^gradegroup/create', Group.create_grade_group),
)
