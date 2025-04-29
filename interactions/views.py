from rest_framework import generics, permissions, status
from .models import CourseReview, LessonComment, LessonLike , Like
from .serializers import CourseReviewSerializer, LessonCommentSerializer, LessonLikeSerializer ,LessonSerializer
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.throttling import AnonRateThrottle
from .throttle import CommentRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType

class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view,obj):
        return request.method in SAFE_METHODS or obj.user == request.user


class CourseReviewListCreateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseReviewSerializer
    permission_classes = [permissions.IsAuthenticated,IsOwnerOrReadOnly]

    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        return CourseReview.objects.filter(course_id=course_id).order_by("-created_at")
    

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, course_id=self.kwargs.get("course_id"))



class LessonCommentListCreateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LessonCommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    throttle_classes = [CommentRateThrottle]

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



class ToggleLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]


    def post(self, request):
        model_type = request.data.get("type")
        obj_id = request.data.get("id")

        