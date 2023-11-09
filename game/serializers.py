from rest_framework import serializers
from .models import Game

class GameSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    correct_answer = serializers.CharField(max_length=100)
    option1 = serializers.CharField(max_length=100)
    option2 = serializers.CharField(max_length=100)
    option3 = serializers.CharField(max_length=100)
    class Meta:
        model = Game
        fields = ['name', 'correct_answer', 'option1', 'option2', 'option3']


class GameDisplaySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    option1 = serializers.CharField(max_length=100)
    option2 = serializers.CharField(max_length=100)
    option3 = serializers.CharField(max_length=100)
    audio_1 = serializers.URLField(max_length=200)
    audio_2 = serializers.URLField(max_length=200)

    class Meta:
        model = Game
        fields = ['name', 'id','option1', 'option2', 'option3','audio_1','audio_2']

class CheckAnswerSerializer(serializers.ModelSerializer):
    answer = serializers.CharField(max_length=100)
    class Meta:
        model = Game
        fields = ['answer']
