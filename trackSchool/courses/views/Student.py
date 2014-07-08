from django.contrib import auth
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from courses.forms import StudentForm, LoginForm, JoinSchoolForm, StudentItemForm, CourseItemForm, AssignmentTypeForm
from courses.models import Student, School, CourseItem, StudentItem, Section, AssignmentType, StudentSection
from courses.methods import send_mail
from trackSchool.settings import SITE_ADDR
from django.contrib.auth.decorators import login_required
import datetime
from gradeGroup.models import Membership
from Grades import update_grades

def create_student(request):
    """
    form for creating a new student
    """
    if request.method == 'POST':
        username = request.POST['email']
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
                    student_form.cleaned_data['email'], student_form.cleaned_data['password'])

                user.last_name = student_form.data['last_name']
                user.first_name = student_form.cleaned_data['first_name']
                user.save()

                student = Student(user=user)

                student.save()

                login_user = auth.authenticate(username=student_form.cleaned_data['username'],
                                               password=student_form.cleaned_data['password'])

                auth.login(request, login_user)

                return redirect("/student/join_school")

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

    title = "Confirm .edu Email Address with Whiteboard"

    content = """<a href="{0}">Please confirm your .edu email address!</a><br>""".format(
        """{0}/confirm_email/{1}/{2}/""".format(SITE_ADDR, str(p.confirmation_code), user.username)
    )
    send_mail(title, content, 'no-reply@%s.com' % SITE_ADDR, [user.email], fail_silently=False)

@login_required
def confirm_edu_email(request, confirmation_code, username):

    user = User.objects.get(username=username)

    student = get_object_or_404(Student, user=user)

    if student.confirmation_code == confirmation_code and user.date_joined > (datetime.datetime.now()-datetime.timedelta(days=1)):
        user.is_active = True
        user.save()
        student.verified_edu_email = True
        student.save()

    return redirect("/student/dashboard")

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

                return redirect("/student/dashboard")

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

@login_required
def show_student(request, pk):

    if pk is None:

        errors = ['No student selected']

        return render_to_response('Student/not_found', {'errors': errors},
                                  RequestContext(request))

    user = get_object_or_404(User, id=pk)

    student = get_object_or_404(Student, user=user)
    
    sections = student.current_courses.all()

    return render_to_response('Student/profile.html', {'student': student, 'sections':sections}, RequestContext(request))


def show_student_groups(request):

    return render_to_response('Student/groups.html', RequestContext(request))


def forgot_password(request):
    return render_to_response('Student/forgot_password.html')

@login_required
def show_dashboard(request):
    """
    show the dashboard with an overview of courses the user is in
    """
    student = get_object_or_404(Student, user = request.user)

    sections = student.current_courses.all().extra(order_by = ["course__title"])

    assignments = student.assignments.all().extra(order_by = ["courseitem__due_date"]).exclude(state="Complete")

    memberships = Membership.objects.filter(student=student)

    student_item_form = StudentItemForm(initial={'state':'Complete'})
    
    grades = student.assignments.filter(state="Complete")

    return render_to_response('Student/dashboard.html', {'student': student,'sections':sections,
        'assignments': assignments,'student_item_form': student_item_form, 'memberships': 
        memberships, 'grades': grades}, RequestContext(request))

def logout(request):

    auth.logout(request)

    return redirect('/')

@login_required
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

                        return redirect("/student/dashboard")
                    else:
                        errors.append("Your email doesn't match the school you selected.")
                        form = school_form = JoinSchoolForm(initial={'email': email})

                        return render_to_response(
                            'Student/join_school.html', {'form': form, 
                            'message': message, 'email': email, 
                            'errors': errors}, RequestContext(request))
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
            return redirect("/student/dashboard")
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

    studentitem = StudentItem.objects.create(courseitem=courseitem, state=0, score=None)
    student.assignments.add(studentitem)

    return redirect("/course/section/"+str(courseitem.courseInstance.pk))

@login_required
def remove_student_item(request,studentitem_pk):
    student = get_object_or_404(Student, user=request.user)
    studentitem = get_object_or_404(StudentItem, id=studentitem_pk)

    student.assignments.remove(studentitem)

    studentitem.delete()
    return redirect("/course/section/"+str(studentitem.courseitem.courseInstance.pk))

@login_required
def edit_assignment(request, studentitem_pk):
    if request.POST:

        student_item_form = StudentItemForm(request.POST)
        if student_item_form.is_valid():
            student_item = StudentItem.objects.get(pk=studentitem_pk)
            student_item.score = student_item_form.cleaned_data['score']
            student_item.state = student_item_form.cleaned_data['state']
            student_item.description = student_item_form.cleaned_data['description']
            student_item.assignment_type = student_item_form.cleaned_data['assignment_type']

            student_item.save(update_fields=['score', 'state', 'description', 'assignment_type'])
            student = get_object_or_404(Student, user=request.user)
            # Update the grades since we possibly changed point values
            # Could be optimized for speed if the score or assignment type wasn't changed.
            update_grades(student.pk, student_item.courseitem.courseInstance.pk)

            return redirect("/course/section/"+str(student_item.courseitem.courseInstance.pk))
        else:
            print "form not valid"
            studentitem = StudentItem.objects.get(pk=studentitem_pk)
            return render_to_response("Student/edit_studentitem.html", {'student_item_form': student_item_form,
                                        'studentitem':studentitem}, RequestContext(request))
    else:
        form = StudentItemForm(initial={'state':'Complete'})

        studentitem = get_object_or_404(StudentItem,id=studentitem_pk)

        return render_to_response("Student/edit_studentitem.html", {'student_item_form': form,
                                    'studentitem':studentitem}, RequestContext(request))

@login_required
def show_grades(request):
    student = get_object_or_404(Student, user=request.user)
    
    sections = list(student.current_courses.all())
    student_assignments = student.assignments.all().filter(state="Complete")
    section_grades = []
    
    for section in sections:
        try:
            assignments = get_list_or_404(student_assignments, 
                courseitem__courseInstance=section.course)
        except:
            assignments = None
        student_section = StudentSection.objects.get(pk=section.pk)
        overall_grade = student_section.grade
        assignment_types = AssignmentType.objects.filter(student=student, sectionInstance=section)
        section_grades.append((section,assignments,assignment_types,overall_grade))
    
    return render_to_response("Student/grades.html", {'student': student, 
        'sections': sections, 'section_grades':section_grades}, RequestContext(request))
    
def add_assignment_type(request, section_pk):
    section = get_object_or_404(Section, pk=section_pk)
    student = get_object_or_404(Student, user=request.user)
    
    if request.POST:
        assignment_type_form = AssignmentTypeForm(request.POST)
        if assignment_type_form.is_valid():
            assignment_type, created = AssignmentType.objects.get_or_create(
                sectionInstance=section,weight=assignment_type_form.cleaned_data['weight'],
                name = assignment_type_form.cleaned_data['name'],student=student)
            assignment_type.weight = assignment_type_form.cleaned_data['weight']
            assignment_type.name = assignment_type_form.cleaned_data['name']
            assignment_type.save()
            
            return redirect('/course/section/'+ str(section_pk))    
        else:
            return redirect('/student/add_assignment_type/'+str(section.id))    
    else:
        assignment_type_form = AssignmentTypeForm()

        return render_to_response("Student/assignment_type.html", 
            {'assignment_type_form':assignment_type_form, 'section':section},
            RequestContext(request))