from django import forms
from django.contrib.auth.models import User

class StudentForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'username', 'password')
        widgets = {'password': forms.PasswordInput()}

class LoginForm(forms.Form):
  class Meta:
    model = User
    fields = ('username', 'password')
    widgets = { 'password': forms.PasswordInput() }