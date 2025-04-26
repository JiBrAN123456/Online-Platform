from rest_framework import serializers
from .models import Course, Lesson, Enrollment
from users.models import User


class LessonSerializer(serializers.ModelSerializer):
     
     class Meta:
          model = Lesson
          fields = ["id", 'title', 'video_url', 'content', 'order']



class InstructorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'profile_picture']



class CourseSerializer(serializers.ModelSerializer):
    instructor_name = InstructorSerializer(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'price', 'image', 'created_at', 'instructor_name', 'lessons']

   

class EnrollmentSerializer(serializers.ModelSerializer):
       
      class Meta:
        fields = ['id', 'student', 'course', 'enrolled_at']
        read_only_fields = ['enrolled_at']