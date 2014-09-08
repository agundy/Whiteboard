from rest_framework import serializers
from models import School, Course, Student
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
    user = serializers.PrimaryKeyRelatedField(many=False)
    school = serializers.PrimaryKeyRelatedField(many=False)
    assignments = serializers.PrimaryKeyRelatedField(many=True)
    current_courses = serializers.PrimaryKeyRelatedField(many=True)
    past_courses = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = Student
        fields = ('user', 'school', 'edu_email', 'assignments', 'current_courses', 'past_courses')


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
    class Meta:
        model = Course
        fields = ('title', 'dept', 'courseID', 'school', 'credits')

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