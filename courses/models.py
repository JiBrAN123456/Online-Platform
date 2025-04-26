from django.db import models
from users.models import User


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'instructor'})
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to="course_images/", blank= True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
       return self.title


class Lesson(models.Model):

    course = models.ForeignKey(Course, on_delete=models.CASCADE ,related_name = "lessons") 
    title = models.CharField(max_length=50)
    video_url = models.URLField(unique=True,blank=True,null=True)
    content = models.TextField(blank = True)
    order = models.PositiveIntegerField(default=1)


    def __str__(self):
        return f"{self.title} - {self.course.title}"




class Enrollment(models.Model):    
    student = models.ForeignKey(User,on_delete=models.CASCADE ,  limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Lesson , on_delete=models.CASCADE )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student" , "course")

    def __str__(self):
        return f"{self.student.email} enroleld in {self.course.title}"    
