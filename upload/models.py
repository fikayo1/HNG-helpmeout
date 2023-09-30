from django.db import models
from cloudinary_storage.storage import VideoMediaCloudinaryStorage


class videos(models.Model):
    title = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now=True)
    video = models.ImageField(upload_to="HNG_Videos", storage=VideoMediaCloudinaryStorage())
    transcipt = models.TextField(default='null', null=True, blank=True)

    def __str__(self):
        return self.title
