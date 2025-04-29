from django.urls import path
from .views import (
    CourseReviewListCreateView,
    LessonCommentListCreateView,
    LessonLikeCreateView,
)

urlpatterns = [
    # Course Reviews
    path('courses/<int:course_id>/reviews/', CourseReviewListCreateView.as_view(), name='course-reviews'),

    # Lesson Comments
    path('lessons/<int:lesson_id>/comments/', LessonCommentListCreateView.as_view(), name='lesson-comments'),

    # Lesson Likes
    path('lessons/<int:lesson_id>/like/', LessonLikeCreateView.as_view(), name='lesson-like'),
]
