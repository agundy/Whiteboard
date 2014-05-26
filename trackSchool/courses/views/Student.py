from django.contrib import auth
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from courses.forms import StudentForm, LoginForm, JoinSchoolForm
from courses.models import Student, School, CourseItem, StudentItem
from courses.methods import send_mail
from trackSchool.settings import SITE_ADDR
from django.contrib.auth.decorators import login_required
import datetime


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

            # print student_form.cleaned_data

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

                return HttpResponseRedirect("/student/join_school")

        else:
            errors = student_form.errors

            return render_to_response('Student/create_student.html', {'form': student_form, 'errors': errors},
                                          RequestContext(request))

    else:

        student_form = StudentForm()

        return render_to_response('Student/create_student.html', {'form': student_form},
                                  RequestContext(request))


def send_edu_email_confirmation(user):
    p = user.student

    title = "Confirm .edu Email Address with 4xB"

    content = """<a href="{0}">Please confirm your .edu email address!</a><br>""".format(
        """{0}/confirm_email/{1}/{2}/""".format(SITE_ADDR, str(p.confirmation_code), user.username)
    )
    send_mail(title, content, 'no-reply@%s.com' % SITE_ADDR, [user.email], fail_silently=False)


def confirm_edu_email(request, confirmation_code, username):

    user = User.objects.get(username=username)

    student = get_object_or_404(Student, user=user)

    if student.confirmation_code == confirmation_code and user.date_joined > (datetime.datetime.now()-datetime.timedelta(days=1)):
        user.is_active = True
        user.save()
        student.verified_edu_email = True
        student.save()

    return HttpResponseRedirect("/student/dashboard")

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

    return render_to_response('Student/groups.html', RequestContext(request))


def forgot_password(request):
    return render_to_response('Student/forgot_password.html')

def show_dashboard(request):
    """
    show the dashboard with an overview of courses the user is in
    """
    student = get_object_or_404(Student, user = request.user)

    sections = student.current_courses.all()

    return render_to_response('Student/dashboard.html', {'student': student,
                                'sections':sections }, RequestContext(request))

def logout(request):

    auth.logout(request)

    return HttpResponseRedirect('/')

def join_school(request):
    """
    Each Student must verify that they actually attend their University
    A student doesn't have to use the .edu email as their account email,
    but they must verify that they have access to one
    """
    errors = []
    message = ""

    if request.POST:
        if 'now' in request.POST:
            if request.POST['school'] != '':
                print request.POST
                school = School.objects.get(pk=request.POST['school'])
                print school
                data = {'school': school.pk,
                        'email': request.POST['email']}
                form = JoinSchoolForm(data)

                if form.is_valid():
                    school = form.cleaned_data['school']

                    email = form.cleaned_data['email']

                    if email.split("@")[1] == school.email_domain:
                        student = get_object_or_404(Student, user=request.user)
                        student.school = school
                        student.save()
                        #send_edu_email_confirmation(request.user)

                        return HttpResponseRedirect("/student/dashboard")
                    else:
                        errors.append("Your email doesn't match the school you selected.")
                        form = school_form = JoinSchoolForm(initial={'email': email})

                        return render_to_response('Student/join_school.html', {'form': form,
                                                                       'message': message,
                                                                       'email': email,
                                                                       'errors': errors},
                                                  RequestContext(request))
                else:
                    school_form = JoinSchoolForm()

                    email = ""

                    errors.append("Invalid Form")

                    return render_to_response('Student/join_school.html', {'form': school_form,
                                                                       'message': message,
                                                                       'email': email,
                                                                       'errors': errors},
                                          RequestContext(request))
            else:
                errors = ["Please Select a School"]

                email = request.POST['email']

                form = school_form = JoinSchoolForm(initial={'email': email})

                return render_to_response('Student/join_school.html', {'form': form,
                                                               'message': message,
                                                               'email': email,
                                                               'errors': errors},
                                          RequestContext(request))
        else:
            # if they don't try verifying their email right now
            print "Join School Later"
            return HttpResponseRedirect("/student/dashboard")
    else:
        student = get_object_or_404(Student, user=request.user)

        if ".edu" in request.user.email.lower():
            email = request.user.email
            message = "It looks like you registered with a .edu email address, " \
                      "smart thinking!"
        else:
            email = None
            message = "Select your school and enter a matching .edu email address."

        school_form = JoinSchoolForm(initial={'email': email, 'school': None})

        return render_to_response('Student/join_school.html', {'form': school_form,
                                                               'message': message,
                                                               'email': email,
                                                               'errors': errors},
                                  RequestContext(request))


@login_required
def add_student_item(request, courseitem_pk):
    
    student = get_object_or_404(Student, user=request.user)
    courseitem = get_object_or_404(CourseItem, id=courseitem_pk)
    
    students_items = student.assignments.all()
    item_list = list(students_items)
    
    for item in item_list:
        print item
    
    try:
        studentitem = StudentItem.objects.create(courseitem=courseitem, state=0, score=1)
        student.assignments.add(studentitem)
    except:
        print "Already Added"
        
    return HttpResponseRedirect("/course/section/"+str(courseitem.courseInstance.pk))