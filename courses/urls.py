from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseListCreateView, CourseDetailView, 
    EnrollCourseView, MyEnrollmentsView, EnrollmentViewSet, 
    MarkLessonCompletedView
)

router = DefaultRouter()
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')

urlpatterns = [
    # Course related
    path('', CourseListCreateView.as_view(), name='course-list-create'),
    path('<int:id>/', CourseDetailView.as_view(), name='course-detail'),
    
    # Enrollment related (custom actions)
    path('enroll/', EnrollCourseView.as_view(), name='course-enroll'),
    path('my-enrollments/', MyEnrollmentsView.as_view(), name='my-enrollments'),
    path('check-enrollment/', MyEnrollmentsView.as_view(), name='check-enrollment'),
    path('enrollments/<int:enrollment_id>/lessons/<int:lesson_id>/complete/', MarkLessonCompletedView.as_view(), name='mark-lesson-complete'),

    # DRF router urls
    path('', include(router.urls)),
]
