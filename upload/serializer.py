from rest_framework import serializers
from .models import videos


class videoUploadSerializer(serializers.ModelSerializer):
    video = serializers.FileField(required=True)
    title = serializers.CharField(required=True)

    class Meta:
        model = videos
        fields = '__all__'