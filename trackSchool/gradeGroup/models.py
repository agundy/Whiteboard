from django.db import models
from django.contrib.auth.models import User
from courses.models import Student, StudentItem
from django.shortcuts import get_object_or_404

class GradeGroup(models.Model):
    name = models.CharField(max_length=128)

    creator = models.ForeignKey(User, blank=True, null=True)

    members = models.ManyToManyField(Student, through='Membership')

    size = models.IntegerField(default=0)

    def add_member(self, user_in, permission):
        """
        adds a user to the group and sets his/her permissions
        """
        student = get_object_or_404(Student, user=user_in)

        print self

        membership = Membership(student=student, group=self, permission=permission)

        membership.save()

        self.size+=1

        self.save()

    def __unicode__(self):
        return self.name


class Membership(models.Model):
    student = models.ForeignKey(Student)

    group = models.ForeignKey(GradeGroup)

    date_joined = models.DateField(auto_now_add=True)

    permission = models.CharField(choices=[('student', "basic member"), ('admin', "group administrator"),
                                            ('creator', "founding member")],
                                  max_length=36)

    def __unicode__(self):
        return str(self.student) + " in " + self.group.name


class GradeReport(models.Model):
    student = models.ForeignKey(Student)

    group = models.ForeignKey(GradeGroup)

    status = models.CharField(choices=[('draft', "waiting to submit"), ('submitted', "report has been sent"),
                                        ('updated', "report has been revised since submission")],
                              max_length=128, default='draft')

    date_created = models.DateTimeField(auto_now_add=True)

    last_updated = models.DateTimeField(auto_now=True)

    grades = models.ManyToManyField(StudentItem, blank=True)

    def __unicode__(self):
        return "Report from " + str(self.student.user) + " at " + self.last_updated
