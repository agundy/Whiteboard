from django import forms
from django.contrib.auth.models import User
from models import GradeGroup


class GroupForm(forms.Form):
	model = GradeGroup
	name = forms.CharField()

	class Meta:
		model = GradeGroup
		fields = ('name')