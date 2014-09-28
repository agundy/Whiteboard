from django.test import TestCase
from django.contrib.auth.models import User
from courses.models import Student


class CoursesViewsTestCases(TestCase):

    """
    docstring for CoursesViewsTestCases
    """

    def setUp(self):
        user = User.objects.create_user(
            'temporary', 'temporary@email.com', 'temporary')
        student = Student(user=user)
        student.save()

    def test_index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_dashboard(self):
        self.client.login(username='temporary@gmail.com', password='temporary')
        resp = self.client.get('/student/dashboard', follow=True)
        self.assertEqual(resp.status_code, 200)
