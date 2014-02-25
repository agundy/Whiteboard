from django.conf.urls import patterns, include, url
from courses.views import *

urlpatterns = patterns('',

    # Student
    url(r'^student/create', Student.create_student),
    url(r'^student/login', Student.login),




    url(r'^gradegroup/create', Group.create_grade_group),
)
