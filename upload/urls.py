from django.urls import path
from .views import *

urlpatterns = [
    path('upload-chunk/', UploadVideosView.as_view(), name='upload'),
    
    #path('upload/', VideoChunkUploadView.as_view(), name='video-list-create'),
]
