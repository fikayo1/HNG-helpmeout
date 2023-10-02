from django.db import models
from cloudinary_storage.storage import VideoMediaCloudinaryStorage
import uuid


class Video(models.Model):
    record_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    combined_video = models.FileField(upload_to='combined_videos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    transcript = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.title

class VideoChunk(models.Model):
    video = models.ForeignKey(Video, related_name='chunks', on_delete=models.CASCADE)
    chunk = models.BinaryField(null=True)




