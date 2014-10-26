from django.conf.urls import patterns, include, url
from gradeGroup.views import *


urlpatterns = patterns('',

    url(r'^create_group', create_grade_group),
    url(r'^delete_group/(\d+)$', delete_grade_group),
    url(r'^$', group_list),
    url(r'^profile/(\d+)$', show_group),
    url(r'^leave/(\d+)$', leave_group),
    url(r'^join/(\d+)$', join_group),
    url(r'^create_report/(\d+)$', create_GradeReport),
    url(r'^edit_report/(\d+)$', edit_GradeReport),
    url(r'^bad_access/$', bad_access),
)
