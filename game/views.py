from random import choice

import cloudinary
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.renderers import UserRenderer
from music.models import Song

from .models import Game, Score
from .serializers import (CheckAnswerSerializer, GameDisplaySerializer,
                          GameSerializer, ScoreSerializer)
from random import sample

class GameList(APIView):

    renderer_classes = (UserRenderer,)
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        audio_clips = Game.objects.all()
        audio_clips = choice(audio_clips)
        serializer = GameDisplaySerializer(audio_clips,)
        return Response({"data": serializer.data, "message": "all songs data succesfully sent"})

    def post(self, request):
            random_songs = list(Song.objects.order_by('?')[:4])

            
            shuffled_songs = sample(random_songs, len(random_songs))

            options = [{
                'name': song.name,
                'audio_url': song.song_url
            } for song in shuffled_songs]

            option1 = options[0]['name']
            option2 = options[1]['name']
            option3 = options[2]['name']
            option4 = options[3]['name']

            correct_answer = options[0]['name']  
            audio1_url = options[0]['audio_url']

            game = Game.objects.create(
                name="Guess the song",
                audio_1=audio1_url,
                option1=option1,
                option2=option2,
                option3=option3,
                option4=option4,
                correct_answer=correct_answer
            )

            game_serializer = GameSerializer(game)
            return Response({"message": game_serializer.data }, status=status.HTTP_201_CREATED)


class CheckAnswer(APIView):
    renderer_classes = (UserRenderer,)
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, pk):
        try:
            audio_clip = Game.objects.get(pk=pk)
        except:
            return Response({"message": "song not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = request.user
            score = Score.objects.get(user=user)
        except:
            score = Score.objects.create(user=user)
        serializer = CheckAnswerSerializer(data=request.data)
        if serializer.is_valid():
            answer = request.data.get('answer')
            correct_answer = audio_clip.correct_answer
            if answer == correct_answer:
                score.score += 1
                score.save()
                return Response({"message": "correct answer"})
            else:
                score.score -= 1
                score.save()
                return Response({"message": "wrong answer"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ScoreList(APIView):
    renderer_classes = (UserRenderer,)
    parser_classes = [MultiPartParser, FormParser]
    def get(self, request):
        scores = Score.objects.all()
        serializer = ScoreSerializer(scores, many=True)
        return Response({"message": serializer.data})

    