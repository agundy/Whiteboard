from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from models import Student


def test_Student_models(self):
    """
    test if a student was created properly

    """
    students = Student.objects.all()

    for user in User.objects.all():
        assert get_object_or_404(Student, use=user)


