from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import base64
import os
from moviepy.editor import VideoFileClip
from io import BytesIO
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Video, VideoChunk
from .serializer import VideoSerializer
from django.http import JsonResponse
from django.conf import settings
import glob
import io

#transcription
import moviepy.editor as mp
import speech_recognition as sr

class UploadVideosView(APIView):
    permission_classes = []
    parser_classes = [JSONParser]

    def post(self, request):
        try:
            data = request.data  # Request data is already parsed as JSON

            # Retrieve fields from the JSON data
            record_id = data.get('record_id')
            chunk_base64 = data.get('chunk_base64')
            chunk_no = int(data.get('chunk_no'))
            final = data.get('final')  #checks if its the final data
            title = data.get('title', "null")

            # Convert Base64 string to binary data
            chunk_binary = base64.b64decode(chunk_base64)

            try:
                video = Video.objects.get(record_id=record_id)
            except Video.DoesNotExist:
                video = Video.objects.create(title=title, record_id=record_id)

            

            if chunk_no == 1:
                # For the first chunk, create a new VideoChunk object
                VideoChunk.objects.create(video=video, chunk=chunk_binary)
            else:
                # For subsequent chunks, append to the existing VideoChunk object
                video_chunk = VideoChunk.objects.get(video=video)
                video_chunk.chunk += chunk_binary
                print(len(video_chunk.chunk))
                video_chunk.save()

            if final == 'true':
                # This is a finalization request, combine all chunks into a single video

                # Retrieve all video chunks and sort them by chunk number
                video_chunks = VideoChunk.objects.filter(video=video).order_by('id')

                # Create a binary stream to hold the combined video
                combined_video_binary = io.BytesIO()

                # Concatenate the binary data of all video chunks
                for chunk in video_chunks:
                    print(chunk)
                    combined_video_binary.write(chunk.chunk)

                combined_video_binary.seek(0)

                # Save the combined video to a file
                combined_video_path = f'media/combined_videos/{record_id}.mp4'
                with open(combined_video_path, 'wb') as combined_file:
                    combined_file.write(combined_video_binary.read())

                # Update the Video model with the combined video path
                video.combined_video = f'combined_videos/{record_id}.mp4'
                video.save()

                # Construct the complete URL using MEDIA_URL
                combined_video_url = f"{settings.MEDIA_URL}{video.combined_video}"

                # Delete the temporary VideoChunk objects
                VideoChunk.objects.filter(video=video).delete()

                #transcription
                # Load the video
                raw_video = combined_video_path
                
                videomp = mp.VideoFileClip(raw_video)

                # Extract the audio from the video
                audio_file = videomp.audio
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
                video.transcript = text
                video.save()

                data = {
                    "record_id": video.record_id,
                    "title": video.title,
                    "combined_video": combined_video_url,
                    "created_at": video.created_at,
                    "transcript": video.transcript
                }
                return Response(data=data)

            return Response({'message': 'Chunk uploaded successfully'})

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        """Get all the recorded videos and their data"""
        try:
            videos = Video.objects.all()
            serializer = VideoSerializer(videos, context={'request': request}, many=True)

            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        except:
            return JsonResponse({"error":"No video uploaded"}, status=status.HTTP_404_NOT_FOUND, safe=False)

    

