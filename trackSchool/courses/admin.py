from models import *
from django.contrib import admin
from django.contrib.auth.models import User, Group

class CourseAdmin(admin.ModelAdmin):
	list_display = ('title', 'dept', 'courseID')
		

for model in (
    School,
    Student,
    # Course,
):
    admin.site.register(model)

admin.site.register(Course, CourseAdmin)