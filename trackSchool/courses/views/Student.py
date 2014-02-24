from django.contrib import auth
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from courses.forms import StudentForm
from courses.models import Student


def create_student(request):

    if request.method == 'POST':
        student_form = StudentForm(request.POST)

        if student_form.is_valid():

            if Student.objects.filter(email=student_form.cleaned_data['email']).len != 0:

                clean_form = StudentForm()

                errors = ['Error: Email in use']

                return render_to_response('Student/create_student.html', {'form': clean_form, 'errors': errors})

            else:

                user = User.object.create(student_form.cleaned_data['first_name'],
                                          student_form.cleaned_data['email'],
                                          student_form.cleaned_data['password'])

                user.last_name = student_form.cleaned_data['last_name']

                user.save()

                student = Student(user)

                return render_to_response('Student/create_success.html', {'student': student})

        else:

                return render_to_response('Student/create_student.html', {'form': student_form})

    else:

        student_form = StudentForm()

        return render_to_response('Student/create_student.html', {'form': student_form})


