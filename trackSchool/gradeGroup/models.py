from django.db import models
from django.contrib.auth.models import User
from courses.models import Student
from django.shortcuts import get_object_or_404

class GradeGroup(models.Model):
    name = models.CharField(max_length=128)

    creator = models.ForeignKey(User, blank=True, null=True)

    members = models.ManyToManyField(Student, through='Membership')

    def add_member(self, user_in, permission):
        """
        adds a user to the group and sets his/her permissions
        """
        student = get_object_or_404(Student, user=user_in)

        print self

        membership = Membership(person=student, group=self, permission=permission)

        membership.save()

    def __unicode__(self):
        return self.name


class Membership(models.Model):
    person = models.ForeignKey(Student)

    group = models.ForeignKey(GradeGroup)

    date_joined = models.DateField(auto_now_add=True)

    permission = models.CharField(choices=[('student', "basic member"), ('admin', "group administrator"),
                                            ('creator', "founding member")],
                                  max_length=36)

    def __unicode__(self):
        return str(self.person) + " in " + self.group.name
