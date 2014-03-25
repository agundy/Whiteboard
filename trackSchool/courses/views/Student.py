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
        username = request.POST['email'].split("@")[0]
        data = {'first_name': request.POST['first_name'],
                'last_name': request.POST['last_name'],
                'email': request.POST['email'],
                'username': username,
                'password': request.POST['password']}

        student_form = StudentForm(data)

        if student_form.is_valid():  # Verify form is complete, correct data

            print student_form.cleaned_data

            student_form.clean()

            if len(User.objects.filter(email=student_form.cleaned_data['email'])) != 0:
            # Make sure email isn't already in use

                clean_form = StudentForm()

                errors = ['Error: Email in use']

                return render_to_response('Student/create_student.html', {'form': clean_form, 'errors': errors},
                                          RequestContext(request))

            elif student_form.cleaned_data['email'] != request.POST['confirm_email']:
                
                errors = ['Error: Emails don\'t match']

                clean_form = Student(request.POST)

                return render_to_response('Student/create_student.html', {'form': clean_form, 'errors': errors},
                                          RequestContext(request))

            elif student_form.cleaned_data['password'] != request.POST['confirm_password']:

                errors = ['Error: Passwords don\'t match']

                clean_form = Student(request.POST)

                return render_to_response('Student/create_student.html', {'form': clean_form, 'errors': errors},
                                          RequestContext(request))

            else:

                user = User.objects.create_user(student_form.cleaned_data['username'],
                                                student_form.cleaned_data['email'],
                                                student_form.cleaned_data['password'])

                user.last_name = student_form.data['last_name']

                user.first_name = student_form.cleaned_data['first_name']
                user.save()

                student = Student(user=user)

                student.save()

                login_user = auth.authenticate(username=student_form.cleaned_data['username'],
                                               password=student_form.cleaned_data['password'])

                auth.login(request, login_user)

                return HttpResponseRedirect("/student/dashboard")

        else:
            errors = ['*']

            return render_to_response('Student/create_student.html', {'form': student_form, 'errors': errors},
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


def show_student(request, pk):

    if pk is None:

        errors = ['No student selected']

        return render_to_response('Student/not_found', {'errors': errors},
                                  RequestContext(request))

    user = get_object_or_404(User, id=pk)

    student = get_object_or_404(Student, user=user)


    return render_to_response('Student/profile.html', {'student': student}, RequestContext(request))

def show_student_groups(request):

    return render_to_response('Student/groups.html',RequestContext(request))

def forgot_password(request):
    return render_to_response('Student/forgot_password.html')

def show_dashboard(request):

    return render_to_response('Student/dashboard.html', RequestContext(request))

def logout(request):

    auth.logout(request)

    return HttpResponseRedirect('/')
