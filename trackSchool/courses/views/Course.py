from django.contrib import auth
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from courses.forms import CourseForm, CreateSectionForm, CourseItemForm, StudentItemForm
from courses.models import Course, Student, Section, CourseItem, AssignmentType, StudentSection
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from datetime import date, datetime
from Grades import update_grades

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
                dept=course_form.cleaned_data['dept'].upper(), courseID=
                course_form.cleaned_data['courseID'], defaults={'title': course_form.cleaned_data['title']})

            return render_to_response('Course/create_success.html', {'course': course},
                                      context_instance=RequestContext(request))
        else:
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

    course = get_object_or_404(Course, id=pk)

    courseItems = CourseItem.objects.filter(courseInstance=pk)
    return render_to_response('Course/profile.html', {'course': course, "courseItems": courseItems,
                               'sections': sections }, RequestContext(request))

@login_required
def show_student_courses(request):
    """
    show the courses a student is enrolled in
    """
    student = get_object_or_404(Student, user = request.user)

    sections = student.current_courses.all()

    return render_to_response('Course/student_courses.html', {'sections': sections },
        RequestContext(request))

@login_required
def browse_courses(request):
    """
    Allow the browsing of available courses
    """
    student = get_object_or_404(Student, user=request.user)
    courses = ""

    if student.school == None:
        enrolled = False
    else:
        enrolled = True
        courses = Course.objects.filter(school=student.school)

    return render_to_response('Course/browse_courses.html', {'enrolled': enrolled,
                                                             'courses': courses,
                                                             'school': student.school}, RequestContext(request))

@login_required
def show_section(request,pk):
    """
    Show a Course Section. 
    """

    if pk is None:
        errors = ['No Section to Display']
        return render_to_response('Course/not_found')

    student = get_object_or_404(Student, user=request.user)
    section = get_object_or_404(Section,id=pk)
    course = get_object_or_404(Course,id=section.course_id)

    enrollment = Student.objects.filter(current_courses = section).count()
    student_items = student.assignments.filter(courseitem__courseInstance=section.id)
    excluded_items = student_items.values_list('courseitem_id', flat=True)
    courseItems = CourseItem.objects.filter(courseInstance=section.id).exclude(id__in=excluded_items)
    
    try: 
        student.current_courses.get(id = section.id)
        enrolled = True

    except:
        enrolled = False

    student_item_form_pair = []
    for student_item in list(student_items):
        student_item_form_pair.append((student_item,StudentItemForm(student=student,
            section=student_item.courseitem.courseInstance,initial={'state':'Complete'})))
    course_item_form = CourseItemForm()
    weights = AssignmentType.objects.filter(student=student,sectionInstance=section)
        
    # Return the page with the results and data
    return render_to_response('Course/section_profile.html', {'course': course, 
        'section': section, 'enrollment': enrollment,'enrolled': enrolled, 
        'courseItems': courseItems,'studentItems': student_item_form_pair,
        'course_item_form':course_item_form, 'weights': weights}, RequestContext(request))

@login_required()
def join_section(request, pk):
    '''
    Add a student to the course
    '''

    if pk is None:
        print "Error no course"
        errors = ['No course selected']
        return render_to_response('Course/section_not_found.html', {'errors': errors}, RequestContext(request))
    student = get_object_or_404(Student, user=request.user)
    section = get_object_or_404(Section, id=pk)
    student.current_courses.add(section)
    
    #StudentSection Creation
    student_section = StudentSection.objects.get_or_create(section=section,student=student)
    update_grades(student.pk,section. pk)
    return redirect("/course/section/"+str(section.id) )

@login_required()
def leave_section(request, pk):
    '''
    Add a student to the course
    '''

    if pk is None:
        print "Error no course"

        errors = ['No course selected']

        return render_to_response('Course/section_not_found.html', {'errors': errors}, RequestContext(request))

    student = get_object_or_404(Student, user=request.user)
    section = get_object_or_404(Section, id=pk)
    try:
        student_section = get_object_or_404(StudentSection, section=section)
        student_section.delete()
    except:
        print "Could not find student section"
    
    # Remove the section from the students current sections
    student.current_courses.remove(section)
    return redirect("/course/section/"+str(section.id) )

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
            section.slug = slugify(section.course.dept+str(section.course.courseID)+str(section.id_no))
            section.save()

            return redirect('/course/profile/'+str(course.pk))
        else:
            errors = ['Do not have all the information']
            print form.errors

            form = CreateSectionForm()
            return render_to_response('Course/add_section.html', {'form': form,'course': \
                            course, 'errors': errors}, RequestContext(request))
    else:
        form = CreateSectionForm(initial={'course': str(course)})
        return render_to_response('Course/add_section.html', {'course': course,
                                    'form': form}, RequestContext(request))

@login_required
def add_assignment(request, pk):
    section = get_object_or_404(Section, id=pk)
    
    if request.POST:
        form = CourseItemForm(request.POST)
        
        if form.is_valid():
            slug = slugify(form.cleaned_data['name'])
            due_date = datetime.combine(form.cleaned_data['due_date'], form.cleaned_data['due_time'])
            
            assignment, created = CourseItem.objects.get_or_create(name=form.cleaned_data['name'],
                                                            due_date= due_date,
                                                            point_value = form.cleaned_data['point_value'],
                                                            courseInstance= section,
                                                            slug=slug)
            return redirect('/course/section/' +str(section.pk))
        else:
            errors = form.errors
            return render_to_response("Course/add_assignment.html", {'section': section,
                                        'form': form,'errors': errors}, RequestContext(request))
    else:
        course_item_form = CourseItemForm()
        
        return render_to_response("Course/add_assignment.html", {'section': section,
                                    'course_item_form': course_item_form}, RequestContext(request))