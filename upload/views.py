from .serializer import videoUploadSerializer
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from django.http import JsonResponse
from .models import videos

#transcription
import moviepy.editor as mp
import speech_recognition as sr



class UploadVideoVIew(APIView):
    permission_classes = []
    parser_classes = [MultiPartParser]
    serializer_class = videoUploadSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        #saving the video and getting the instance
        video_obj = serializer.save()

        # Load the video
        raw_video = video_obj.video.url 
        #raw_video = serializer.data['video']
        video = mp.VideoFileClip(raw_video)

        # Extract the audio from the video
        audio_file = video.audio
        audio_file.write_audiofile("audio.wav")

        # Initialize recognizer
        r = sr.Recognizer()

        # Load the audio file
        with sr.AudioFile("audio.wav") as source:
            data = r.record(source)
        
        try:
            # Convert speech to text
            text = r.recognize_google(data)
        except sr.UnknownValueError:
            print("Google Web speech API could not understand the audio")
        except sr.RequestError as e:
            print("could not request results from Google web speech Api; {}".format(e))
        
        # Print the text
        print("\nThe resultant text from video is: \n")
        print(text)

        # Assign the transcript to the video object and save it
        video_obj.transcipt = text
        print(video_obj.title)
        video_obj.save()

        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        """Get all the recorded videos and their data"""
        try:
            video = videos.objects.all()
            serializer = self.serializer_class(video, context={'request': request}, many=True)

            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        except:
            return JsonResponse({"error":"No video uploaded"}, status=status.HTTP_404_NOT_FOUND, safe=False)