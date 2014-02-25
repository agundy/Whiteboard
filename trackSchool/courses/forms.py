from django import forms
from django.contrib.auth.models import User
from courses.models import GradeGroup

class StudentForm(forms.Form):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')
        widgets = {'password': forms.PasswordInput()}

class GroupForm(forms.Form):
    class Meta:
        model = GradeGroup
        fields = ('name',)

class LoginForm(forms.Form):
  class Meta:
    model = User
    fields = ('email', 'password')
    widgets = { 'password': forms.PasswordInput() }