from __future__ import division
from courses.models import Student, Section, CourseItem, AssignmentType, StudentSection
import datetime

def update_grades(student_pk, section_pk):
    student = Student.objects.get(pk=student_pk)
    section = Section.objects.get(pk=section_pk)
    student_section = StudentSection.objects.get(section=section,student=student)
    assignment_types = list(AssignmentType.objects.filter(student=student,sectionInstance=section))
    
    aggregate_grades = []
    # go through each assignment type for the section
    for assignment_type in assignment_types:
        # Get a list of all of the assignments for this type ie all homeworks
        assignments = list(student.assignments.filter(assignment_type=assignment_type, courseitem__courseInstance=section))
        total_possible = 0
        total_score = 0
        
        for assignment in assignments:
            # if an assignment is marked as complete then use it's data
            if assignment.state == 'Complete':
                total_possible += assignment.courseitem.point_value
                total_score += assignment.score
        if total_possible > 0:
            assignment_type.aggregate_grade = total_score/total_possible * 100
            assignment_type.save()
            aggregate_grades.append((assignment_type.weight, total_score/total_possible))
    overall_grade = 0
    overall_percent = 0
    for aggregate_grade in aggregate_grades:
        overall_grade += aggregate_grade[0]*aggregate_grade[1]
        overall_percent += aggregate_grade[0]
    # overall_grade = relatie percent of grade finishished so far
    # overall_percent = percent of grade counted
    # overall_grade/overall_percent = relative grade
    if overall_percent > 0:
        student_section.grade = overall_grade/overall_percent *100
    student_section.save()


def update_priority(student_pk):
    student = Student.objects.get(pk=student_pk)
    student_sections = list(StudentSection.objects.filter(student=student)) 
 
    """ Course_Difficulty & Assignment_Difficulty variables are needed"""

    for section in student_sections:
        assignment_types = list(AssignmentType.objects.filter(sectionInstance = section))
        credits = section.course.credits
        course_grade = section.grade
        if course_grade == 0:
            course_grade = 0.01
        """Big_Score = Course_Diff*credits/course_grade"""
        for assignment_type in assignment_types:
            assignments = list(student.assignments.filter(assignment_type=assignment_type, 
                courseitem__courseInstance=section, state='Incomplete'))   
            weight = assignment_type.weight
            assignmenttype_grade = assignment_type.aggregate_grade
            for assignment in assignments: 
                time_left = (assignment.courseitem.due_date - datetime.now()).total_seconds()/3600                     
                if time_left <= 0.000:      
                    assignment.state = 'Late'
                    assignment.save()
                    time_left = 0.01
                """Little_Score = Assignment_Diff*weight/time_left/assignmenttype_grade"""

                Score = Big_Score + Little_Score  
                assignment.priority = Score
                assignment.save()
