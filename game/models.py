from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=100)
    audio_1 = models.URLField(max_length=200,default=None,blank=True,null=True)
    correct_answer = models.CharField(max_length=100)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)

    def __str__(self):
        return self.name
