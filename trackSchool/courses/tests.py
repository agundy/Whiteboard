from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from models import Student, CourseObject


def test_Student_models(self):
    """
    test if a student was created properly

    """
    students = Student.objects.all()

    for user in User.objects.all():
        assert get_object_or_404(Student, use=user)


def create_CourseObject(self):
    """
    test creation of a CourseObject
    """


    course_object = CourseObject(type="exam", name="exam 1")

    course_object.due_date = "4/7/2018"

    course_object.save()

    assert get_object_or_404(CourseObject, name="exam 1")