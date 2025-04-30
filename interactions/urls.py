from django.urls import path
from .views import (
    CourseReviewListCreateView,
    LessonCommentListCreateView,
    LessonLikeCreateView,
    ToggleLikeView, 
    LessonCommentRetrieveUpdateDestroyView ,BookmarkDeleteView , BookmarkListCreateView
)

urlpatterns = [
    # Course Reviews
    path('courses/<int:course_id>/reviews/', CourseReviewListCreateView.as_view(), name='course-reviews'),

    # Lesson Comments
    path('lessons/<int:lesson_id>/comments/', LessonCommentListCreateView.as_view(), name='lesson-comments'),
    path('lesson-comments/', LessonCommentListCreateView.as_view(), name='lesson-comment-list-create'),
    path('lesson-comments/<int:pk>/', LessonCommentRetrieveUpdateDestroyView.as_view(), name='lesson-comment-detail'),


    # Lesson Likes
    path('lessons/<int:lesson_id>/like/', LessonLikeCreateView.as_view(), name='lesson-like'),
    path("like/", ToggleLikeView.as_view(), name="toggle-like"),
    
    # Bookmark 
    path('bookmarks/', BookmarkListCreateView.as_view(), name='bookmark-list-create'),
    path('bookmarks/<int:pk>/', BookmarkDeleteView.as_view(), name='bookmark-delete'),
]
