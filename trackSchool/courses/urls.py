from django.conf.urls import patterns, include, url
from courses.views import *
from django.views.generic import TemplateView

urlpatterns = patterns('',

    # Student
    url(r'^student/create', Student.create_student),
    url(r'^student/join_school/$', Student.join_school),
    url(r'^student/dashboard', Student.show_dashboard),
    url(r'^confirm_email/(?P<confirmation_code>\w{0,50})/(?P<username>\w{0,50})/$',Student.confirm_edu_email),
    url(r'^accounts/login', Student.login),
    url(r'^accounts/logout', Student.logout),
    url(r'^student/profile/(\d+)$', Student.show_student),
    url(r'^student/profile/$', Student.show_student),
    url(r'^student/groups/',Student.show_student_groups),
    url(r'^student/grades/', Student.show_grades),
    url(r'^student/js_grades/', Student.js_grades),
    url(r'^student/edit/', Student.edit_student),
    url(r'^student/add_assignment/(\d+)$',Student.add_student_item),
    url(r'^student/remove_assignment/(\d+)$',Student.remove_student_item),
    url(r'^student/edit_assignment/(\d+)$',Student.edit_assignment),
    url(r'^student/add_assignment_type/(\d+)$', Student.add_assignment_type),
    url(r'^forgot-password', Student.forgot_password),
    # Course
    url(r'^course/create', Course.create_course),
    url(r'^course/student_dashboard', Student.show_dashboard),
    url(r'^course/students_courses', Course.show_student_courses),
    url(r'^course/browse', Course.browse_courses),
    url(r'^course/profile/(\d+)$', Course.show_course),
    url(r'^course/section/join/(\d+)$', Course.join_section),
    url(r'^course/section/leave/(\d+)$', Course.leave_section),
    url(r'^course/section/add_assignment/(\d+)$', Course.add_assignment),
    url(r'^course/add_section/(?P<course>\w{0,50})$', Course.add_section),
    url(r'^course/section/(\d+)$', Course.show_section)
)