from django.conf.urls import patterns, include, url
from gradeGroup.views import *


urlpatterns = patterns('',

    url(r'^create', create_grade_group),
    url(r'^$', group_list),
    url(r'^profile/(\d+)$', show_group),
)
