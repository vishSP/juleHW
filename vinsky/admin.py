from django.contrib import admin
from vinsky.models import Сourse, Lesson

@admin.register(Сourse)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'preview', 'text','author')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'preview', 'text', 'link', 'course', 'author')