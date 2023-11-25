from django.db import models

from accounts.models import MyUser


class Game(models.Model):
    name = models.CharField(max_length=100)
    audio_1 = models.URLField(max_length=200,default=None,blank=True,null=True)
    correct_answer = models.CharField(max_length=100)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100,default=None,blank=True,null=True)
    option4 = models.CharField(max_length=100,default=None,blank=True,null=True)
    def __str__(self):
        return f"{self.id}"

class Score(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-score']
