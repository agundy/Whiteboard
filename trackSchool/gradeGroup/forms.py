from django import forms
from django.contrib.auth.models import User
from models import GradeGroup


class GroupForm(forms.Form):
    class Meta:
        model = GradeGroup
        fields = ('name',)

