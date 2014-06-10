from models import *
from django.contrib import admin
from django.contrib.auth.models import User

class GradeGroupAdmin(admin.ModelAdmin):
	fields = ['name','creator']
	list_display = ('name','creator')

for model in (
    Membership,
	GradeReport
    # GradeGroup
):
    admin.site.register(model)

admin.site.register(GradeGroup, GradeGroupAdmin)
