from models import *
from django.contrib import admin
from django.contrib.auth.models import User

for model in (
    Membership,
    GradeGroup
):
    admin.site.register(model)

