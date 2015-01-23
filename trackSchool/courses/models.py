from django.db import models
from django.contrib.auth.models import User


class School(models.Model):
    name = models.CharField(max_length=256, blank=False)
    email_domain = models.CharField(max_length=256, blank=False)
    website = models.URLField(max_length=256)

    def __unicode__(self):
        """
        outputs name of School
        """
        return self.name


class Course(models.Model):
    """
    A course is just the generic college course with it's name/id number/department and the like
    """
    title = models.CharField(max_length=256)
    dept = models.CharField(max_length=6)
    courseID = models.CharField(max_length=16)
    school = models.ForeignKey(School)
    credits = models.IntegerField(default=4)

    def __unicode__(self):
        """
        outputs name of course
        """
        return self.dept + " " + self.courseID + ": " + self.title


class Section(models.Model):
    '''
    Sections are instances of a course and are individualize to the professor and times
    '''
    term_choices = [('Winter', 'Winter'), ('Spring', 'Spring'),
                    ('Summer', 'Summer'), ('Fall', 'Fall')]
    year = models.IntegerField()
    term = models.CharField(max_length=10, choices=term_choices)
    course = models.ForeignKey(Course)
    professor = models.CharField(max_length=256)
    id_no = models.CharField(max_length=16)
    slug = models.SlugField(null=False)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        """
        outputs course name, term and year when print/str is called
        """
        return str(self.id) + " " \
            + str(self.course) + " " + self.term + ", " + str(self.year)

    def short_name(self):
        return str(self.course.dept) + " " + str(self.course.courseID)


class CourseItem(models.Model):
    """
    Stores base course item with generic assignment details
    """
    name = models.CharField(max_length=50)
    courseInstance = models.ForeignKey(Section)
    due_date = models.DateTimeField()
    point_value = models.IntegerField()
    slug = models.SlugField(unique=False, null=False)

    def __unicode__(self):
        """
        outputs name and description

        """
        return str(self.name)


class StudentItem(models.Model):
    '''
    Based off of a course item but stores a students personal data
    '''
    DIFFICULTY_CHOICES = (
        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
        (6, 6), (7, 7), (8, 8), (9, 9), (10, 10))
    state_choices = [
        ('Incomplete', 'Incomplete'),
        ('Complete', 'Complete'),
        ('Late', 'Late')]
    courseitem = models.ForeignKey(CourseItem)
    score = models.IntegerField(blank=True, null=True)
    # 0 = uncompleted
    # 1 = completed
    # 2 = Late
    state = models.CharField(max_length=20, choices=state_choices, null=False)
    description = models.CharField(max_length=256, blank=True)

    assignment_type = models.ForeignKey(
        'AssignmentType', null=True,
        related_name='student_item_assignment_type')

    # Data for prioritizing homework
    assignment_difficulty = models.IntegerField(
        default=5, choices=DIFFICULTY_CHOICES)

    priority = models.FloatField(default=0)

    def __unicode__(self):
        """
        outputs name of course item

        """
        return str(self.courseitem) + " - " + str(self.courseitem.courseInstance)



class AssignmentType(models.Model):
    """
    Students grouping of weighted assignments
    """
    sectionInstance = models.ForeignKey(Section)
    name = models.CharField(max_length=15)
    weight = models.FloatField()
    student = models.ForeignKey('Student')
    aggregate_grade = models.FloatField(default=0)
    total_graded_points = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.name)


class Student(models.Model):
    user = models.OneToOneField(User)
    school = models.ForeignKey(School, null=True)
    edu_email = models.EmailField(null=True)
    confirmation_code = models.CharField(max_length=256, null=True)
    verified_edu_email = models.BooleanField(default=False)
    assignments = models.ManyToManyField(StudentItem)
    current_courses = models.ManyToManyField(
        Section, related_name='current_courses')
    past_courses = models.ManyToManyField(Section, related_name='past_courses')

    def __unicode__(self):
        """
        outputs name of student

        """
        return self.user.first_name + " " + self.user.last_name


class StudentSection(models.Model):
    student = models.ForeignKey(Student)
    section = models.ForeignKey(Section)
    grade = models.FloatField(default=100)


class BetaUser(models.Model):

    """
        Model Used to Save Who wants a beta invite.
    """
    first_name = models.CharField(max_length=256,)
    last_name = models.CharField(max_length=256,)
    school = models.CharField(max_length=256, null=True)
    edu_email = models.EmailField(null=True)
    request_date = models.DateTimeField(null=True)

    def __unicode__(self):
        return self.first_name
