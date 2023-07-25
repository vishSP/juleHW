from django.contrib import admin
from vinsky.models import Сourse, Lesson, Subscription


@admin.register(Сourse)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'preview', 'text', 'user')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'preview', 'text', 'link', 'course', 'user')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id','course', 'user', 'payment', 'status')
