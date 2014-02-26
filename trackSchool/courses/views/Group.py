from django.contrib import auth
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from courses.forms import GroupForm
from courses.models import GradeGroup, Membership


def create_grade_group(request):
    """
    Form for creating a new group
    """

    user = request.user

    if not user.is_authenticated:

        clean_form = GroupForm()

        errors = ['Error: You must be authenticated to create a group']

        return render_to_response('Group/create_group.html', {'form': clean_form, 'errors': errors})

    if request.method == 'POST':

        group_form = GroupForm(request.POST)

        if group_form.is_valid():  # Verify form data is correct

            if GradeGroup.objects.all.filter(name=group_form.cleaned_data['name']).len != 0:
            # Make sure group name doesn't already exist

                clean_form = GroupForm()

                errors = ['Error: Group Name in use']

                return render_to_response('Group/create_group.html', {'form': clean_form, 'errors': errors})

            else:

                group = GradeGroup.objects.create(group_form.cleaned_data['name'])

                group.add_user(user, 'admin')

                group.creator = user

                group.save()

                return render_to_response('Group/create_success.html', {})

        else:

            clean_form = GroupForm()

            errors = ['Error: Invalid input']

            return render_to_response('Group/create_group.html', {'form': clean_form, 'errors': errors})

    else:

        clean_form = GroupForm()

        errors = []

        return render_to_response('Group/create_group.html', {'form': clean_form, 'errors': errors})

def show_group(request, *args, **kwargs):
    """
    display a group's page
    @param kwargs: pk (group primary key)
    """
    group_key = args[0]

    if group_key is None:

        errors = ['Unable to find group']

        return render_to_response('Group/not_found', {}, RequestContext(reqest))

    # Lookup Group

    group = get_object_or_404(GradeGroup, pk=group_key)

    members = Membership.objects.filter(group=group)

    return render_to_response('Group/profile.html', {'group': group, 'members': members},
                              RequestContext(request))


def group_list(request):
    """
    a view to list all groups
    """

    groups = GradeGroup.objects.all()

    return render_to_response('Group/list.html', {'groups': groups},
                              RequestContext(request))


