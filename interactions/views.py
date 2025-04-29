from rest_framework import generics, permissions
from .models import CourseReview, LessonComment, LessonLike
from .serializers import CourseReviewSerializer, LessonCommentSerializer, LessonLikeSerializer



class CourseReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = CourseReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        return CourseReview.objects.filter(course_id=course_id).order_by("-created_at")
    

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, course_id=self.kwargs.get("course_id"))



class LessonCommentListCreateView(generics.ListCreateAPIView):
    serializer_class = LessonCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        lesson_id = self.kwargs.get("lesson_id")
        return LessonComment.objects.filter(lesson_id=lesson_id).order_by("-created_by")
    

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, lesson_id=self.kwargs.get("lesson_id"))



class LessonLikeCreateView(generics.CreateAPIView):
    serializer_class = LessonLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, lesson_id=self.kwargs.get('lesson_id'))
