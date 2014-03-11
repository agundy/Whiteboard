from django.conf.urls import patterns, include, url
from courses.views import *
from django.views.generic import TemplateView

urlpatterns = patterns('',

    # Student
    url(r'^student/create', Student.create_student),
    url(r'^student/dashboard', Student.show_dashboard),
    url(r'^student/login', Student.login),
    url(r'^student/logout', Student.logout),
    url(r'^student/profile/(\d+)$', Student.show_student),
    url(r'^student/profile/$', Student.show_student),
    url(r'^student/groups',Student.show_student_groups),
    url(r'^forgot-password', Student.forgot_password),
    url(r'^course/create', Course.create_course),
    url(r'^course/student_dashboard', Course.show_student_dashboard)
)
