from django.contrib import admin
from vinsky.models import Сourse, Lesson, Subscription


@admin.register(Сourse)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'preview', 'text', 'author')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'preview', 'text', 'link', 'course', 'author')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'status')
