from django.db import models
from django.contrib.auth.models import User


class School(models.Model):
    name = models.CharField(max_length=256, blank=False)

    email_domain = models.CharField(max_length=256, blank=False)

    website = models.URLField(max_length=256)


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

    def __unicode__(self):
        """
        outputs name of course
        """
        return self.dept + " " + self.courseID + ": " + self.title


class CourseSection(models.Model):
    term_choices = [(1, 'winter'), (2, 'spring'), (3, 'summer'), (4, 'fall')]

    year = models.IntegerField()

    term = models.CharField(max_length=16, choices=term_choices)

    course = models.ForeignKey(Course)

    professor = models.CharField(max_length=256)

    # content = document()


class CourseItem(models.Model):
    name = models.CharField(max_length=256)

    courseInstance = models.ForeignKey(Course)

    due_date = models.DateTimeField()
