from django.db import models
from users.models import User
from courses.models import Course, Lesson
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings




class CourseReview(models.Model):
      course = models.ForeignKey(Course, on_delete=models.CASCADE , related_name="reviews")
      user = models.ForeignKey(User, on_delete=models.CASCADE , related_name= "course_reviews")
      rating = models.PositiveIntegerField()
      review = models.TextField()
      created_at = models.DateTimeField(auto_now_add=True)


      class Meta:
            unique_together = ('course', 'User')
            ordering = ("-created_at")


      def __str__(self):
            return f"{self.user.email} - {self.course.title} - {self.rating} stars "

class LessonComment(models.Model):

      lesson = models.ForeignKey(Course , on_delete=models.CASCADE , related_name= "commnets")
      user = models.ForeignKey(CourseReview.user, on_delete=models.CASCADE , related_name= "lesson_comments")
      comment = models.TextField()
      created_at = models.DateTimeField(auto_now_add=True)
      
      updated_at = models.DateTimeField(auto_now=True)
      is_edited = models.BooleanField(default=False)
      parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name="replies")

      class Meta:
            ordering = ["-created_at"]

      
      def __str__(self):
            return f"{self.user.email} - {self.lesson.title}"
      
    
      def save(self, *args, **kwargs):
         if self.pk:  # If the comment already exists and is being updated
             self.is_edited = True
         super().save(*args, **kwargs)


class LessonLike(models.Model):        
      
      lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE , related_name= "likes")
      user = models.ForeignKey(User , on_delete=models.CASCADE , related_name= "lesson_likes")
      created_at = models.DateTimeField(auto_now_add=True)

      class Meta:
            unique_together = ('lesson',"user")


      def __str__(self):
            return f"{self.user.email} liked  {self.lesson.title}"      




class Like(models.Model):
      user = models.ForeignKey(User, on_delete=models.CASCADE)
      content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
      object_id = models.PositiveIntegerField()
      content_object = GenericForeignKey("content_type" , "object_id")
      created_at = models.DateTimeField(auto_now_add=True)


      class Meta:
            unique_togetehr = ('user','content_type','object_id')

            