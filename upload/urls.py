from django.urls import path
from .views import *


urlpatterns = [
    path('upload', UploadVideoVIew.as_view(), name='upload')
]