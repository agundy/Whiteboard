from django.test import TestCase
from django.contrib.auth.models import User
from courses.models import Student
from models import Student, CourseItem


class CoursesViewsTestCases(TestCase):

def test_student_models(self):
    """
    test if a student was created properly
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


def create_courseitem(self):
    """
    test creation of a CourseObject
    """
    course_object = CourseItem(type="exam", name="exam 1")
    course_object.due_date = "4/7/2018"
    course_object.save()
    assert get_object_or_404(CourseItem, name="exam 1")
