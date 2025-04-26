from django.urls import path
from .views import CourseListCreateView, CourseDetailView, EnrollCourseView

urlpatterns = [
    path('', CourseListCreateView.as_view(), name='course-list-create'),              # No 'courses/' prefix here
    path('<int:id>/', CourseDetailView.as_view(), name='course-detail'),
    path('enroll/', EnrollCourseView.as_view(), name='course-enroll'),
]
