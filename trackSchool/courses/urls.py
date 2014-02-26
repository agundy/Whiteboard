from django.conf.urls import patterns, include, url
from courses.views import *
from django.views.generic import TemplateView

urlpatterns = patterns('',

    # Student
    url(r'^student/create', Student.create_student),
    url(r'^student/login', Student.login),
    url(r'^student/profile/(\d+)$', Student.show_student),
    url(r'^student/profile/$', Student.show_student),

)
