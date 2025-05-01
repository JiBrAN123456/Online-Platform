from rest_framework import serializers
from .models import CourseReview, LessonComment, LessonLike, Like, Lesson , Bookmark , Course , Notification
from django.contrib.contenttypes.models import ContentType


# ──────────────── Course Review ────────────────

class CourseReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = CourseReview
        fields = ['id', 'course', 'user', 'user_name', 'rating', 'review', 'created_at', 'review_count']
        read_only_fields = ['id', 'user', 'created_at', 'user_name']

    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def get_review_count(self, obj):
        return CourseReview.objects.filter(course=obj.course).count()

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value


# ──────────────── Lesson Comments ────────────────

class LessonCommentSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    comments_count = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = LessonComment
        fields = ['id', 'lesson', 'user', 'user_name', 'comment', 'created_at', 'likes_count', 'comments_count', 'replies']
        read_only_fields = ['id', 'user', 'created_at', 'user_name']

    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def get_comments_count(self, obj):
        return obj.replies.count() if hasattr(obj, 'replies') else 0

    def get_replies(self, obj):
        replies = obj.replies.all()
        return LessonCommentSerializer(replies, many=True, context=self.context).data


# ──────────────── Lesson Like ────────────────

class LessonLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonLike
        fields = ['id', 'lesson', 'user', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


# ──────────────── Lesson Serializer ────────────────

class LessonSerializer(serializers.ModelSerializer):
    total_likes = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'video_url', 'created_at', 'total_likes', 'is_liked' , "is_bookmarked"]  # Add actual fields from your model

    def get_total_likes(self, obj):
        content_type = ContentType.objects.get_for_model(Lesson)
        return Like.objects.filter(content_type=content_type, object_id=obj.id).count()

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Like.objects.filter(
                user=user,
                content_type=ContentType.objects.get_for_model(Lesson),
                object_id=obj.id
            ).exists()
        return False

    
    def get_is_bookmarked(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return Bookmark.objects.filter(
                user=user,
                content_type = ContentType.objects.get_for_model(Lesson),
                object_id = obj.id
            ).exists()
        return False



class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
       model = Bookmark
       fields = ['id', 'user', 'content_type', 'object_id', 'created_at']
       read_only_fields = ['id', 'user', 'created_at']


class CourseSerializer(serializers.ModelSerializer):
    instructor_name = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'price', 'image', 'created_at', 'instructor_name', 'lessons', 'is_bookmarked']


        def get_instructor_name(self,obj):
            return f"{obj.instructor.first_name} {obj.instructor.last_name}"
        
        def get_is_bookmarked(self,obj):
            user = self.context["request"].user
            if user.is_authenticated:
                return Bookmark.objects.filter(
                    user=user,
                    content_type= ContentType.objects.get_for_model(Course),
                    object = obj.id

                ).exists()
            return False
        


class NotificationSerializer(serializers.ModelSerializer):
      
      actor_name = serializers.SerializerMethodField()
      target_type = serializers.SerializerMethodField()

      class Meta:
          model = Notification
          fields =  ['id', 'recipient', 'actor', 'actor_name', 'verb',
            'target_type', 'object_id', 'description', 'url',
            'is_read', 'timestamp']

          read_only_fields = fields     

          def get_actor_name(self, obj):
             return f"{obj.actor.first_name} {obj.actor.last_name}"

          def get_target_type(self, obj):
             return obj.content_type.model if obj.content_type else None