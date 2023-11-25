from rest_framework import serializers

from .models import *


class GameSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    correct_answer = serializers.CharField(max_length=100)
    option1 = serializers.CharField(max_length=100)
    option2 = serializers.CharField(max_length=100)
    option3 = serializers.CharField(max_length=100)
    option4 = serializers.CharField(max_length=100)
    audio_1 = serializers.URLField(max_length=200)
    class Meta:
        model = Game
        fields = ['id','name', 'correct_answer', 'option1', 'option2', 'audio_1','option3','option4']


class GameDisplaySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    option1 = serializers.CharField(max_length=100)
    option2 = serializers.CharField(max_length=100)
    option3 = serializers.CharField(max_length=100)
    option4 = serializers.CharField(max_length=100)
    audio_1 = serializers.URLField(max_length=200)

    class Meta:
        model = Game
        fields = ['name', 'id','option1', 'option2','option3','option4','audio_1']

class CheckAnswerSerializer(serializers.ModelSerializer):
    answer = serializers.CharField(max_length=100)
    class Meta:
        model = Game
        fields = ['answer']

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ['user', 'score']
