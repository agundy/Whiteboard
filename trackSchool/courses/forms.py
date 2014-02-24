from django import forms
from django.contrib.auth.models import User

class StudentForm(forms.Form):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')
        widgets = {'password': forms.PasswordInput()}

