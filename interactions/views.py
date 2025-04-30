from rest_framework import generics, permissions, status
from .models import CourseReview, LessonComment, LessonLike , Like ,Lesson 
from .serializers import CourseReviewSerializer, LessonCommentSerializer, LessonLikeSerializer ,LessonSerializer
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.throttling import AnonRateThrottle
from .throttle import CommentRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import PermissionDenied

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

        model_map = {
            "lesson" :Lesson,
            "comment": LessonComment,
        }

        if model_type not in model_map:
            return Response({"error":"Invalid type"}, status=400)
        
        model_class = model_map[model_type]
        content_type = ContentType.objects.get_for_model(model_class)

        like, created = Like.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id= obj_id
        )

        if not created:
            like.delete()
            return Response({"message":"Unliked"}, status=200)
        
        return Response({"message":"Liked"},status=201)
    


class LessonCommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LessonComment.objects.all()
    serializer_class = LessonCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    def perform_update(self, serializer):
        if self.get_object().user != self.request.user:
            raise PermissionDenied("You can only update your own comments")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You can only delete you own commetns")
        instance.delete()
             