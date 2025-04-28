from django.shortcuts import render
from rest_framework import generics, permissions , viewsets
from .models import Course, Lesson, Enrollment , LessonProgress
from .serializers import CourseSerializer, LessonSerializer, EnrollmentSerializer , EnrollmentDashboardSerializer
from .permissions import IsInstructorOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status , filters
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from users.models import Notification
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

class CourseListCreateView(generics.ListCreateAPIView):


      def perform_create(self, serializer):
            serializer.save(instructor=self.request.user)

      def get_permissions(self):
            
            if self.request.method == "POST":
                return [permissions.IsAuthenticated(), permissions.IsAdminUser()] 
            return [permissions.AllowAny()]
            

class CoursePagination(PageNumberPagination):
      page_size = 20
      page_size_query_param = "page_size"
      max_page_size = 50


class CourseListAPIView(generics.ListAPIView):
      queryset = Course.objects.all()
      serializer_class = CourseSerializer
      pagination_class =  CoursePagination
 

      filter_backends = [DjangoFilterBackend , filters.SearchFilter ,filters.OrderingFilter]
      search_filters = ['title', 'description', 'instructor__first_name', 'instructor__last_name']
      filterset_fields = {
            'price' : ["gte", "lte"],
      }
      
      ordering_fields = ['created_at',"price"]
      ordering = ["-created_at"]




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


class MyEnrollmentsView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
          return Enrollment.objects.filter(student= self.request.user)



class EnrollmentViewSet(viewsets.ModelViewSet):

     serializer_class = EnrollmentSerializer
     permission_classes = [permissions.IsAuthenticated]


     def get_queryset(self):
           return Enrollment.objects.filter(user= self.request.user)
     
     def perform_create(self, serializer):
           serializer.save(user= self.request.user)


     @action(detail=True, methods=['delete'], url_path='unenroll')
     def unenroll(self, request, pk=None):
           enrollment = self.get_object()
           enrollment.delete()
           return Response({"detail" : "Sucessfully unenrolled from the course"}, status=status.HTTP_200_OK)


     def check_enrollment(self, request):
            course_id = Course.objects.get(id= course_id)
            if not course_id:
                 return Response({"Response": "Course id is required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                  course = Course.objects.get(id = course_id)
            except:
                  return Response({"detail": "Course not found"}, status=status.HTTP_400_BAD_REQUEST) 

            is_enrolled = Enrollment.objects.get(user= self.request.user , course=course)


            return Response({"is_enrolled": is_enrolled} , status=status.HTTP_200_OK)        


class CourseViewSet(viewsets.ModelViewSet):
      queryset = Course.objects.all()
      serializer_class = CourseSerializer
      permission_classes = [IsInstructorOrReadOnly]            



class MarkLessonCompletedView(APIView):
      permission_classes = [IsAuthenticated]


      def post(self, request, enrollment_id, lesson_id):
          enrollment = Enrollment.objects.get(id = enrollment_id , user= request.user) 
          lesson = Lesson.objects.get(id = lesson_id) 


          progress , created = LessonProgress.objects.get_or_create(enrollment = enrollment , lesson = lesson)
          
          if not progress.completed:
                progress.completed = True
                progress.completed_at = timezone.now()
                progress.save()

                total_lessons = Lesson.objects.filter(course = enrollment.course).count()
                completed_lessons = LessonProgress.objects.filter(enrollment = enrollment, completed = True).count()

                if total_lessons > 0:
                      enrollment.progress = ( completed_lessons/total_lessons) * 100
                      enrollment.save()

                if enrollment.progress == 100:
                      enrollment.status == "completed"
                      enrollment.save()

                return Response({"message": "Lesson marked as completed", "progress": enrollment.progress})

          return Response({"message": "Lesson already completed"})




class StudentDashboardView(generics.ListAPIView):
      serializer_class =  EnrollmentDashboardSerializer
      permission_classes = [IsAuthenticated]


      def get_queryset(self):
            return Enrollment.objects.filter(user= self.request.user)




class FeaturedCoursesAPIView(generics.ListAPIView):
      serializer_class = CourseSerializer


      def get_queryset(self):
            return Course.objects.order_by("created_at")[:5]