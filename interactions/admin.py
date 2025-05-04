from django.contrib import admin
from .models import CourseReview , Course , Lesson , LessonComment , LessonLike , Bookmark , Notification
# Register your models here.

admin.site.register(CourseReview)

admin.site.register(Course)

admin.site.register(Lesson)

admin.site.register(LessonLike)

admin.site.register(LessonComment)

admin.site.register(Bookmark)

admin.site.register(Notification)