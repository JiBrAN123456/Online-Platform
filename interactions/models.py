from django.db import models
from users.models import User
from courses.models import Course, Lesson




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

      class Meta:
            ordering = ["-created_at"]

      
      def __str__(self):
            return f"{self.user.email} - {self.lesson.title}"


class LessonLike(models.Model):        
      
      lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE , related_name= "likes")
      user = models.ForeignKey(User , on_delete=models.CASCADE , related_name= "lesson_likes")
      created_at = models.DateTimeField(auto_now_add=True)

      class Meta:
            unique_together = ('lesson',"user")


      def __str__(self):
            return f"{self.user.email} liked  {self.lesson.title}"      
