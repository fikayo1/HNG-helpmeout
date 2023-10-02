# from rest_framework import serializers
# from .models import videos


# class videoUploadSerializer(serializers.ModelSerializer):
#     video = serializers.FileField(required=True)
#     title = serializers.CharField(required=True)

#     class Meta:
#         model = videos
#         fields = '__all__'


from rest_framework import serializers
from .models import Video

# class VideoChunkSerializerd(serializers.ModelSerializer):
#     class Meta:
#         model = VideoChunk
#         fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = '__all__'


class VideoChunkSerializer(serializers.Serializer):
    record_id = serializers.CharField()
    chunk_base64 = serializers.CharField()
    chunk_no = serializers.IntegerField()
    final = serializers.BooleanField()
    title = serializers.CharField(required=False, default="null")