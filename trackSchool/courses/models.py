from django.db import models
from django.contrib.auth.models import User


class School(models.Model):
    name = models.CharField(max_length=256)


class Student(models.Model):
    user = models.OneToOneField(User)

    def __unicode__(self):
        """
        outputs name of student

        """
        return self.user.first_name + " " + self.user.last_name


class GradeGroup(models.Model):
    name = models.CharField(max_length=128)

    creator = models.ForeignKey(User)

    members = models.ManyToManyField(Student, through='Membership')

    def add_member(self, user, permission):
        """
        adds a user to the group and sets his/her permissions
        """
        student = Student.objects.all.filter(user=user)

        membership = Membership(student=student, group=self, permission=permission)

        membership.save()


class Membership(models.Model):
    person = models.ForeignKey(Student)

    group = models.ForeignKey(GradeGroup)

    date_joined = models.DateField()

    permission = models.CharField(choices=[('student', "basic member"), ('admin', "group administrator")],
                                  max_length=36)


class Course(models.Model):
    title = models.CharField(max_length=256)

    dept = models.CharField(max_length=6)

    courseID = models.CharField(max_length=16)

    crn = models.CharField(max_length=16)


