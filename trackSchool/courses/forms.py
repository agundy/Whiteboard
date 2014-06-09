from django import forms
from django.contrib.auth.models import User
from courses.models import Course, School, Section, CourseItem, StudentItem


class StudentForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'username', 'password')
        widgets = {'password': forms.PasswordInput()}

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True


class CourseForm(forms.Form):
    """docstring for CourseForm"""
    model = Course

    title = forms.CharField(max_length=256)

    dept = forms.CharField(max_length=6)

    courseID = forms.CharField(max_length=16)

    class Meta:
        model = Course
        fields = ('title', 'dept', 'courseID')


class LoginForm(forms.Form):

    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {'password': forms.PasswordInput() }


class JoinSchoolForm(forms.Form):
    email = forms.EmailField(max_length=100)
    school = forms.ModelChoiceField(queryset=School.objects.all())


class CreateSectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ('year', 'term', 'professor', 'id_no', 'course')

class CourseItemForm(forms.Form):
    model = CourseItem

    name = forms.CharField(max_length=256)

    due_date = forms.DateField()
    
    due_time = forms.TimeField()
    
    point_value = forms.IntegerField()
    
    class Meta:
        model = Course
        fields = ('name', 'month', 'day', 'year','time')

class StudentItemForm(forms.ModelForm):
    class Meta:
        model = StudentItem
        fields = ('score', 'state')