from rest_framework import generics, permissions, status
from .models import CourseReview, LessonComment, LessonLike , Like ,Lesson , Bookmark , Notification
from .serializers import CourseReviewSerializer, LessonCommentSerializer, LessonLikeSerializer ,LessonSerializer , BookmarkSerializer , NotificationSerializer
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



class LessonCommentListCreateView(generics.ListCreateAPIView):
    serializer_class = LessonCommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    throttle_classes = [CommentRateThrottle]

    def get_queryset(self):
        lesson_id = self.kwargs.get("lesson_id")
        return LessonComment.objects.filter(lesson_id=lesson_id).order_by("-created_by")
    

    def perform_create(self, serializer):
        comment = serializer.save(user=self.request.user, lesson_id=self.kwargs.get("lesson_id"))

    # Send notification if it's a reply
        if comment.parent:
           if comment.parent.user != self.request.user:
                Notification.objects.create(
                recipient=comment.parent.user,
                actor=self.request.user,
                verb="replied to your comment",
                target=comment.parent
            )


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
             


class BookmarkListCreateView(generics.ListCreateAPIView):
    
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BookmarkDeleteView(generics.DestroyAPIView):
    
  
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return Bookmark.objects.filter(user= self.request.user) 
    



class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)
    

class MarkNotificationAsRead(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Notification.objects.all()

    def patch(self, request, *args, **kwargs):
        notification = self.get_object()
        if notification.recipient != request.user:
           return Response({'error': 'Permission denied'}, status=403)
        notification.is_read = True
        notification.save() 
        return Response({"status" : "marked as read"})    




class MarkAllNotificationsAsRead(APIView):
    permission_classes = [permissions.IsAuthenticated]


    def post(self,request):
        Notification.objects.filter(recipient=request.user , is_read= False).update(is_read=True)
        return Response({"status":"marked as read"}, status=status.HTTP_200_OK)