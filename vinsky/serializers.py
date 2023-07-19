from rest_framework import serializers

from vinsky.models import Сourse, Lesson, Payments, Subscription
from vinsky.validators import VideoValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        validators = [VideoValidator(field='link')]
        fields = (
            "id",
            "title",
            "text",
            "preview",
            "link",
            "author",
        )


class СourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)
    subscription = serializers.SerializerMethodField()
    def get_lessons_count(self, instance):
        lessons = Lesson.objects.filter(course=instance).all()
        if lessons:
            return lessons.count()
        return 0

    def get_subscription(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            course = obj
            subscription = Subscription.objects.filter(course=course, user=user).first()
            if subscription:
                return subscription.status
        return False
    class Meta:
        model = Сourse
        fields = (
            "id",
            "title",
            "preview",
            "description",
            "lessons_count",
            "lessons",
        )


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'