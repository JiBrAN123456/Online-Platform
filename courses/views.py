from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Course, Lesson, Enrollment
from .serializers import CourseSerializer, LessonSerializer, EnrollmentSerializer



class CourseListCreateView(generics.ListCreateAPIView):
      queryset = Course.objects.all()
      serializer_class = CourseSerializer
      
      def perform_create(self, serializer):
            serializer.save(instructor=self.request.user)

      def get_permissions(self):
            
            if self.request.method == "POST":
                return [permissions.IsAuthenticated(), permissions.IsAdminUser() ] 
            return [permissions.AllowAny()]
            

class CourseDetailView(generics.RetrieveAPIView):
      queryset = Course.objects.all()
      serializer_class = CourseSerializer
      lookup_field = "id"                   



class EnrollCourseView(generics.CreateAPIView):
      queryset = Enrollment.objects.all()
      serializer_class = EnrollmentSerializer
      permission_classes = [permissions.IsAuthenticated]


      def perform_create(self, serializer):
            serializer.save(student = self.request.user)