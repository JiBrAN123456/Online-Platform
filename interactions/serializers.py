from rest_framework import serializers
from .models import CourseReview, LessonComment, LessonLike




class CourseReviewSerializer(serializers.ModelSerializer):

     user_name = serializers.SerializerMethodField()
     review_count = serializers.SerializerMethodField()



     def get_user_name(self, obj):
          return f"{obj.user.first_name} {obj.user.last_name}"


     def validate_rating(self, value):
         if not 1 <= value <= 5:
              raise serializers.ValidationError("Ratings must be between1 and 5")
         return value

     def get_review_count(self,obj):
         return obj.reviews.count()


     
     class Meta:
          model = CourseReview
          fields = ['id', 'course', 'user', 'user_name', 'rating', 'review', 'created_at','review_count' ]
          read_only_fields = ['id', 'user', 'created_at', 'user_name', ]


class LessonCommentSerializer(serializers.ModelSerializer):
     user_name = serializers.SerializerMethodField()  
     likes_count = serializers.IntegerField(source='likes.count', read_only=True)
     comments_count = serializers.IntegerField(source='comments.count', read_only=True)


     class Meta:
        model = LessonComment
        fields = ['id', 'lesson', 'user', 'user_name', 'comment', 'created_at','likes_count', 'comments_count']
        read_only_fields = ['id', 'user', 'created_at', 'user_name']

     def get_user_name(self , obj):   
         return f"{obj.user.first_name} {obj.user.last_name}"
 




class LessonLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonLike
        fields = ['id', 'lesson', 'user', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']