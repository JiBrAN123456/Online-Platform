from django.urls import path
from .views import CourseListCreateView, CourseDetailView, EnrollCourseView , MyEnrollmentsView, EnrollmentViewSet
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')


urlpatterns = [
    path('', CourseListCreateView.as_view(), name='course-list-create'),              # No 'courses/' prefix here
    path('<int:id>/', CourseDetailView.as_view(), name='course-detail'),
    path('enroll/', EnrollCourseView.as_view(), name='course-enroll'),
    path('my-enrollments/', MyEnrollmentsView.as_view(), name='my-enrollments'),
    path('check-enrollment/', MyEnrollmentsView.as_view(), name='check-enrollment'),
    router.urls,
]
