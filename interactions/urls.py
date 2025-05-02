from django.urls import path
from .views import (
    CourseReviewListCreateView,
    LessonCommentListCreateView,
    LessonCommentRetrieveUpdateDestroyView,
    LessonLikeCreateView,
    ToggleLikeView,
    BookmarkListCreateView,
    BookmarkDeleteView,
    NotificationListView,
    MarkNotificationAsRead,
    MarkAllNotificationsAsRead,
)

urlpatterns = [
    # ─── Course Reviews ─────────────────────────────
    path('courses/<int:course_id>/reviews/', CourseReviewListCreateView.as_view(), name='course-reviews'),

    # ─── Lesson Comments ────────────────────────────
    path('lessons/<int:lesson_id>/comments/', LessonCommentListCreateView.as_view(), name='lesson-comments'),
    path('lesson-comments/<int:pk>/', LessonCommentRetrieveUpdateDestroyView.as_view(), name='lesson-comment-detail'),

    # ─── Likes ──────────────────────────────────────
    path('lessons/<int:lesson_id>/like/', LessonLikeCreateView.as_view(), name='lesson-like'),
    path('like/', ToggleLikeView.as_view(), name='toggle-like'),

    # ─── Bookmarks ──────────────────────────────────
    path('bookmarks/', BookmarkListCreateView.as_view(), name='bookmark-list-create'),
    path('bookmarks/<int:pk>/', BookmarkDeleteView.as_view(), name='bookmark-delete'),


    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/read/', MarkNotificationAsRead.as_view(), name='notification-mark-read'),
    path('notifications/read-all/',  MarkAllNotificationsAsRead.as_view(), name='notifications-read-all'),
]
