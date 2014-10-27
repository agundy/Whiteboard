from django.contrib import auth
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from forms import GroupForm
from models import GradeGroup, Membership, GradeReport
from courses.models import Student, StudentItem
from django.template.defaultfilters import slugify


@login_required
def create_grade_group(request):
    """
    Form for creating a new group
    """

    user = request.user

    if request.method == 'POST':

        group_form = GroupForm(request.POST)
        if group_form.is_valid():  # Verify form data is correct

            if len(GradeGroup.objects.filter(name=group_form.cleaned_data['name'])) != 0:
            # Make sure group name doesn't already exist

                clean_form = GroupForm()

                errors = ['Error: Group Name in use']

                return render_to_response('Group/create_group.html', {'form': clean_form, 'errors': errors}, context_instance = RequestContext(request))

            else:
                group = GradeGroup(name=group_form.cleaned_data['name'],)

                group.creator = user

                group.save()

                group.add_member(user, 'creator')

                group.save()

                return render_to_response('Group/create_success.html', {'group': group}, context_instance = RequestContext(request))

        else:

            clean_form = GroupForm()

            errors = ['Error: Invalid input']

            return render_to_response('Group/create_group.html', {'form': clean_form, 'errors': errors},context_instance = RequestContext(request))

    else:

        clean_form = GroupForm()

        errors = []

        return render_to_response('Group/create_group.html', {'form': clean_form, 'errors': errors}, RequestContext(request))

@login_required
def delete_grade_group(request, args):
    """
    Form for creating a new group
    """

    errors = []

    group = get_object_or_404(GradeGroup, id=args)

    student = get_object_or_404(Student, user=request.user)

    memberships = Membership.objects.filter(group=group, student=student)

    if(len(memberships) !=0 ):
        if(memberships[0].permission == 'creator'):
            group.delete()
            return render_to_response('Group/delete_success.html', {'group': group, 'errors': errors}, context_instance = RequestContext(request))
        else:
            errors = ['Error: Only group creator can delete group']
            return render_to_response('Group/delete_success.html', {'group': group, 'errors': errors}, context_instance = RequestContext(request))
    else:
        errors = ['Error: Not a group member']
        return render_to_response('Group/delete_success.html', {'group': group, 'errors': errors}, context_instance = RequestContext(request))


def show_group(request, *args, **kwargs):
    """
    display a group's page
    @param kwargs: pk (group primary key)
    """
    group_key = args[0]

    if group_key is None:

        errors = ['Unable to find group']

        return render_to_response('Group/not_found', {}, RequestContext(reqest))

    is_member = False
    is_creator = False
    reports = []

    group = get_object_or_404(GradeGroup, pk=group_key)

    members = Membership.objects.filter(group=group)

    if request.user.is_authenticated():
        student = get_object_or_404(Student, user=request.user)

        # See if the request user is already a member
        for member in members:
            if member.student.user == request.user:
                is_member = True

                reports = GradeReport.objects.filter(group=group, student=member)

                if member.permission == 'creator':
                    is_creator = True

                break

    return render_to_response('Group/profile.html', {'group': group, 'members': members, 'is_member': is_member,
                                                      'is_creator': is_creator, 'reports': reports},
                              RequestContext(request))


def group_list(request):
    """
    a view to list all groups
    """
    groups = GradeGroup.objects.all()

    return render_to_response('Group/list.html', {'groups': groups},
                              RequestContext(request))

@login_required
def join_group(request, group_id):
    """
    add a user to a group
    """
    group = get_object_or_404(GradeGroup, id=group_id)

    group.add_member(request.user, 'student')

    group.save()

    return redirect(show_group, group.id)

@login_required
def leave_group(request, group_id):
    """
    remove a user from a group
    """
    print group_id

    group = get_object_or_404(GradeGroup, id=group_id)

    student = get_object_or_404(Student, user=request.user)

    memberships = Membership.objects.filter(group=group, student=student)

    for member in memberships:
        member.delete()

        group.size -=1

    group.save()

    return redirect(show_group, group_id)

@login_required
def create_GradeReport(request, group_id):
    """
    create a new draft of a GradeReport
    """
    group = get_object_or_404(GradeGroup, id=group_id)

    student = get_object_or_404(Student, user=request.user)

    report = GradeReport(student=student, group=group)

    report.save()

    report.slug = slugify(str(report) + student.user.first_name)

    report.save()

    return redirect(show_group, group.id)

@login_required
def edit_GradeReport(request, report_id):
    """
    edit a GradeReport
    """
    report = get_object_or_404(GradeReport, id=report_id)

    if request.user != report.student.user:
        return redirect(bad_access)

    if request.POST:
        return redirect(show_group, report.group.id)

    return render_to_response('Group/partials/edit_report.html', {'assignments': report.student.assignments},
                              RequestContext(request))


def bad_access(request):
    return render_to_response('bad_access.html')
