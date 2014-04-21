from django.conf.urls import patterns, include, url
from courses.views import *
from django.views.generic import TemplateView

urlpatterns = patterns('',

    # Student
    url(r'^student/create', Student.create_student),
    url(r'^student/join_school/$', Student.join_school),
    url(r'^student/dashboard', Student.show_dashboard),
    url(r'^confirm_email/(?P<confirmation_code>\w{0,50})/(?P<username>\w{0,50})/$', Student.confirm_edu_email),
    url(r'^accounts/login', Student.login),
    url(r'^accounts/logout', Student.logout),
    url(r'^student/profile/(\d+)$', Student.show_student),
    url(r'^student/profile/$', Student.show_student),
    url(r'^student/groups',Student.show_student_groups),
    url(r'^forgot-password', Student.forgot_password),
    url(r'^course/create', Course.create_course),
    url(r'^course/student_dashboard', Course.show_student_dashboard),
    url(r'^course/students_course', Course.show_student_courses),
    url(r'^course/browse', Course.browse_courses),
    url(r'^course/profile/(\d+)$', Course.show_course),
    url(r'^course/join/(\d+)$', Course.join_section),
    url(r'^course/add_section/(?P<course>\w{0,50})$', Course.add_section),
    url(r'^course/section/(\d+)$', Course.show_section)
)
