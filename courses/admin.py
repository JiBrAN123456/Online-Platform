from django.contrib import admin
from . models import Course , LessonProgress , Enrollment , Lesson
# Register your models here.


admin.site.register(Course)

admin.site.register(LessonProgress)

admin.site.register(Lesson)

admin.site.register(Enrollment)
