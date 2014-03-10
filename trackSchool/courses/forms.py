from django import forms
from django.contrib.auth.models import User
from courses.models import Course

class StudentForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'username', 'password')
        widgets = {'password': forms.PasswordInput()}

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True

class CourseForm(forms.ModelForm):
    """docstring for CourseForm"""
    class Meta:
        model = Course
        fields = ('title', 'dept', 'courseID', 'course_unique')

    def __init__(self, arg):
        super(CourseForm, self).__init__()
        self.arg = arg
        

class LoginForm(forms.Form):
  class Meta:
    model = User
    fields = ('username', 'password')
    widgets = { 'password': forms.PasswordInput() }