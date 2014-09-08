from courses.serializers import SchoolSerializer, StudentSerializer
from courses.models import School, Student
from rest_framework import mixins
from rest_framework import generics
from courses.permissions import IsOwnerOrReadOnly


class SchoolList(generics.ListCreateAPIView):
    """
    List all schools
    """
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SchoolDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    List a single school
    """
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class StudentSelfDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Get a student's private profile
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = IsOwnerOrReadOnly

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class StudentDetail(generics.RetrieveDestroyAPIView):
    """
    Get a student's public profile
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class StudentList(generics.ListAPIView):
    """
    List all students
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)