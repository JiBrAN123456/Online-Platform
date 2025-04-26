from django.shortcuts import render
from rest_framework import generics, permissions , viewsets
from .models import Course, Lesson, Enrollment
from .serializers import CourseSerializer, LessonSerializer, EnrollmentSerializer
from .permissions import IsInstructorOrReadOnly


class CourseListCreateView(generics.ListCreateAPIView):
      queryset = Course.objects.all()
      serializer_class = CourseSerializer
      
      def perform_create(self, serializer):
            serializer.save(instructor=self.request.user)

      def get_permissions(self):
            
            if self.request.method == "POST":
                return [permissions.IsAuthenticated(), permissions.IsAdminUser()] 
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



class CourseViewSet(viewsets.ModelViewSet):
      queryset = Course.objects.all()
      serializer_class = CourseSerializer
      permission_classes = [IsInstructorOrReadOnly]            