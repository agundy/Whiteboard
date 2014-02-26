from django.conf.urls import patterns, include, url
from courses.views import *

urlpatterns = patterns('',

    # Student
    url(r'^student/create', Student.create_student),
    url(r'^student/login', Student.login),





    url(r'^gradegroup/create', Group.create_grade_group),
    url(r'^gradegroup/list', Group.group_list),
    url(r'^gradegroup/show/(\d+)$', Group.show_group),
)
