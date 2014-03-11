from django.db import models
from django.contrib.auth.models import User
from courses.models import Student

class GradeGroup(models.Model):
    name = models.CharField(max_length=128)

    creator = models.ForeignKey(User, blank=True, null=True)

    members = models.ManyToManyField(Student, through='Membership')

    def add_member(self, user_in, permission):
        """
        adds a user to the group and sets his/her permissions
        """
        student = Student.objects.filter(user=user_in)

        # membership = Membership(student=student, group=self, permission=permission)

        # membership.save()


class Membership(models.Model):
    person = models.ForeignKey(Student)

    group = models.ForeignKey(GradeGroup)

    date_joined = models.DateField()

    permission = models.CharField(choices=[('student', "basic member"), ('admin', "group administrator")],
                                  max_length=36)