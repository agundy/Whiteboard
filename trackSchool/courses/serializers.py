from rest_framework import serializers
from models import School, Course, Student, Section
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    A serializer for users
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'snippets')


class StudentSerializer(serializers.ModelSerializer):
    """
    A serializer for Students
    """
    user = serializers.RelatedField(many=False)
    school = serializers.RelatedField(many=False)
    assignments = serializers.RelatedField(many=True)
    current_courses = serializers.RelatedField(many=True)
    past_courses = serializers.RelatedField(many=True)

    class Meta:
        model = Student
        fields = ('user', 'school', 'assignments', 'current_courses', 'past_courses')


class SchoolSerializer(serializers.ModelSerializer):
    """
    A serializer to parse school objects
    """
    class Meta:
        model = School
        fields = ('name', 'email_domain', 'website')


class CourseSerializer(serializers.ModelSerializer):
    """
    A serializer to parse courses
    """
    school = serializers.RelatedField(many=False)
    class Meta:
        model = Course
        fields = ('title', 'dept', 'courseID', 'school', 'credits', 'id')

    def validate_school(self, attrs, source):
        """
        Verify a valid school has been supplied
        """
        value = attrs[source]
        try:
            School.objects.get(name=value)
            return attrs
        except School.DoesNotExist:
            serializers.ValidationError('Please enter a valid school')


class SectionSerializer(serializers.ModelSerializer):
    """
    Section Serializer
    """
    course = serializers.RelatedField(many=False)
    class Meta:
        model = Section
        fields = ('year', 'term', 'course', 'professor', 'id_no', 'id')