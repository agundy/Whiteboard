from __future__ import division
from courses.models import Student, Section, AssignmentType, StudentSection

def update_grades(student_pk, section_pk):
    student = Student.objects.get(pk=student_pk)
    section = Section.objects.get(pk=section_pk)
    student_section = StudentSection.objects.get(pk=section_pk)
    
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
    student_section.grade = overall_grade/overall_percent *100
    student_section.save()