from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Game
from .serializers import GameSerializer ,GameDisplaySerializer,CheckAnswerSerializer
from accounts.renderers import UserRenderer
import cloudinary
from rest_framework.parsers import MultiPartParser, FormParser

class GameList(APIView):

    renderer_classes = (UserRenderer,)
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        audio_clips = Game.objects.all()
        serializer = GameDisplaySerializer(audio_clips, many=True)
        return Response({"data":serializer.data,"message":"all songs dagta succesfully sent"})

    def post(self, request):
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            audio1_response = None
            audio2_response = None
            option1 = request.data.get('option1')
            option2 = request.data.get('option2')
            option3 = request.data.get('option3')
            correct_answer = request.data.get('correct_answer')
            if option1 != correct_answer and option2 != correct_answer and option3 != correct_answer:
                return Response({'message': 'one of the option should be equal to the answer'}, status=status.HTTP_400_BAD_REQUEST)
            if 'audio1' in request.data:
                if request.FILES['audio1'].size > 10000000:
                    return Response({'message': 'file size is too large'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'audio1 is required'}, status=status.HTTP_400_BAD_REQUEST)
            if 'audio2' in request.data:
                if request.FILES['audio2'].size > 10000000:
                    return Response({'message': 'file size is too large'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'audio2 is required'}, status=status.HTTP_400_BAD_REQUEST)

            audio1 = request.FILES['audio1']
            audio2 = request.FILES['audio2']
            audio1_response = cloudinary.uploader.upload(audio1, secure=True,resource_type="video")
            audio2_response = cloudinary.uploader.upload(audio2, secure=True,resource_type="video")
            audio1_url = audio1_response.get('url')
            audio2_url = audio2_response.get('url')
            Game.objects.create(
                audio_1 = audio1_url,
                audio_2 = audio2_url,
                **serializer.validated_data
                )
            return Response({"message":serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class GameDetail(APIView):
    renderer_classes = (UserRenderer,)

    def get(self, request, pk):
        audio_clip = Game.objects.get(pk=pk)
        serializer = GameDisplaySerializer(audio_clip)
        return Response(serializer.data)

class CheckAnswer(APIView):
    renderer_classes = (UserRenderer,)
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, pk):
        try:
            audio_clip = Game.objects.get(pk=pk)
        except:
            return Response({"message":"song not found"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CheckAnswerSerializer(data=request.data)
        if serializer.is_valid():
            answer = request.data.get('answer')
            correct_answer = audio_clip.correct_answer
            if answer == correct_answer:
                return Response({"message":"correct answer"})
            else:
                return Response({"message":"wrong answer"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
