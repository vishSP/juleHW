from rest_framework import serializers

from vinsky.models import Сourse


class VideoValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        video_url = value.get('video')
        if video_url and 'youtube.com' not in video_url:
            raise serializers.ValidationError("Только youtube.com ссылки ")


