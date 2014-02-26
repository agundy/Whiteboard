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


class Course(models.Model):
    title = models.CharField(max_length=256)

    dept = models.CharField(max_length=6)

    courseID = models.CharField(max_length=16)

    course_unique = models.CharField(max_length=16)


class CourseInstance(models.Model):
    term_choices = [(1, 'winter'), (2, 'spring'), (3, 'summer'), (4, 'fall')]

    year = models.integerField()

    term = models.CharField(choices=term_choices)

    course = models.ForeignKey(Course)

    professor = models.CharField(max_length=256)

    # content = document()


class CourseItem(models.Model):
    name = models.CharField(max_length=256)

    courseInstance = models.ForeignKey(Course)

    due_date = models.DateTimeField()
