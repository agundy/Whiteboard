from django.contrib import auth
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from courses.forms import StudentForm, LoginForm
from courses.models import Student


def create_student(request):
    """
    form for creating a new student
    """
    if request.method == 'POST':
        student_form = StudentForm(request.POST)

        if student_form.is_valid():  # Verify form is complete, correct data

            if Student.objects.filter(email=student_form.cleaned_data['email']).len != 0:
            # Make sure email isn't already in use

                clean_form = StudentForm()

                errors = ['Error: Email in use']

                return render_to_response('Student/create_student.html', {'form': clean_form, 'errors': errors},
                                          RequestContext(request))

            else:

                user = User.object.create(student_form.cleaned_data['first_name'],
                                          student_form.cleaned_data['email'],
                                          student_form.cleaned_data['password'])

                user.last_name = student_form.cleaned_data['last_name']

                user.save()

                student = Student(user)

                return render_to_response('Student/create_success.html', {'student': student},
                                          RequestContext(request))

        else:

                return render_to_response('Student/create_student.html', {'form': student_form},
                                          RequestContext(request))

    else:

        student_form = StudentForm()

        return render_to_response('Student/create_student.html', {'form': student_form},
                                  RequestContext(request))


def login(request):
    """
    login a user
    """
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth.login(request, user)

                return HttpResponseRedirect("/student/dashboard")

            else:
                errors = ['User disabled']

                login_form = LoginForm()

                return render_to_response('Student/login.html', {'form': login_form, 'errors': errors},
                                          RequestContext(request))
        else:
            errors = ['Invalid Username or Password']

            login_form = LoginForm()

            return render_to_response('Student/login.html', {'form': login_form, 'errors': errors},
                                      RequestContext(request))

    else:

        login_form = LoginForm()

        errors = []

        return render_to_response('Student/login.html', {'form': login_form, 'errors': errors},
                                  RequestContext(request))


def show_student(request, *args, **kwargs):

    user_pk = args[0]

    if user_pk is None:

        errors = ['No student selected']

        return render_to_response('Student/not_found', {'errors': errors},
                                  RequestContext(request))

    user = get_object_or_404(Student, pk=user_pk)

    return render_to_response('Student/profile.html', {'student': user}, RequestContext(request))

def forgot_password(request):
    return render_to_response('Student/forgot_password.html')

def show_dashboard(request):

    return render_to_response('Student/dashboard.html', RequestContext(request))

