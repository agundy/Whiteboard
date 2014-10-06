from models import *
from django.contrib import admin
# from django.contrib.auth.models import User  # , Group



class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'dept', 'courseID')


class CourseItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'courseInstance', 'due_date')

for model in (
    School,
    Student,
    Section,
    StudentItem,
    AssignmentType,
    BetaUser
):
    admin.site.register(model)

admin.site.register(CourseItem, CourseItemAdmin)
admin.site.register(Course, CourseAdmin)
