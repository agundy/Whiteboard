from django.contrib import auth
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from courses.forms import CourseForm, CreateSectionForm
from courses.models import Course, Student, Section, CourseItem
from django.contrib.auth.decorators import login_required
from datetime import date

@login_required
def create_course(request):
    """
    form for creating a new course
    """

    user = request.user

    if not user.is_authenticated:
        clean_form = CourseForm()

        errors = [' Error: You must be authenticated to create a course']
        return render_to_response('Course/create_course.html', {'form': clean_form, 'errors': errors},
                                  context_instance=RequestContext(request))

    if request.method == 'POST':
        data = {'title': request.POST['title'],
                'dept': request.POST['dept'],
                'courseID': request.POST['courseID']}

        course_form = CourseForm(request.POST)

        if course_form.is_valid():
            student = get_object_or_404(Student, user=request.user)
            course, created = Course.objects.get_or_create(school=student.school,
                                                           dept=course_form.cleaned_data['dept'].upper(),
                                                           courseID=course_form.cleaned_data['courseID'],
                                                           defaults={'title': course_form.cleaned_data['title']})

            return render_to_response('Course/create_success.html', {'course': course},
                                      context_instance=RequestContext(request))
        else:
            # print course_form.cleaned_data['title']
            clean_form = CourseForm()

            errors = ['Error: Invalid Input']

            return render_to_response('Course/create_course.html', {'form': clean_form, 'errors': errors},
                                      context_instance=RequestContext(request))

    else:
        # clean_form =
        errors = []

        return render_to_response('Course/create_course.html', RequestContext(request))

@login_required
def show_course(request, pk):
    if pk is None:
        print "Error no course"

        errors = ['No course selected']

        return render_to_response('Course/not_found.html', {'errors': errors}, RequestContext(request))

    sections = Section.objects.filter(course=pk)

    new_course = get_object_or_404(Course, id=pk)

    courseItems = CourseItem.objects.filter(courseInstance=pk)
    return render_to_response('Course/profile.html', {'course': new_course, "courseItems": courseItems,
                               'sections': sections }, RequestContext(request))

@login_required
def show_student_dashboard(request):
    """
    show the dashboard with an overview of courses the user is in
    """

    return render_to_response('Course/student_dashboard.html', RequestContext(request))

@login_required
def show_student_courses(request):
    """
    show the courses a student is enrolled in
    """

    return render_to_response('Course/student_courses.html', RequestContext(request))


@login_required
def browse_courses(request):
    """
    Allow the browsing of available courses
    """
    student = get_object_or_404(Student, user=request.user)
    courses = Course.objects.filter(school=student.school)

    return render_to_response('Course/browse_courses.html', {'courses': courses,
                                                             'school': student.school}, RequestContext(request))


@login_required()
def join_section(request, pk):
    if pk is None:
        print "Error no course"

        errors = ['No course selected']

        return render_to_response('Course/section_not_found.html', {'errors': errors}, RequestContext(request))

    user = request.user

    student = get_object_or_404(Student, user=user)
    section = get_object_or_404(Section, id=pk)
    student.current_courses.add(section)

    return render_to_response('Course/profile.html', {'course': new_course, "courseItems": courseItems},
                              RequestContext(request))


@login_required
def add_section(request, course):
    course = get_object_or_404(Course, pk=course)
    
    if request.POST:
        form = CreateSectionForm(request.POST)
        form.year = date.today().year
        form.course = course.id

        if form.is_valid():
            section = form.save()
            section.course = course
            section.year = date.today().year
            section.save()

            return HttpResponseRedirect('/course/profile/'+str(course.pk))
        else:
            errors = ['Do not have all the information']
            print form.errors

            form = CreateSectionForm()
            return render_to_response('Course/add_section.html', {'form': form,'course': course, 'errors': errors},
                               RequestContext(request))
    else:

        form = CreateSectionForm()
        return render_to_response('Course/add_section.html', {'course': course,
                                    'form': form}, RequestContext(request))
