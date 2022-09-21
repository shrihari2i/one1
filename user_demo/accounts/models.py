from tkinter.tix import Tree
from django.db import models
from django.contrib.auth.models import User
import datetime
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.

class My_score(models.Model):
    player_id=models.IntegerField(default=0)
    myscr = models.CharField(max_length=200, default='vijay')

    def __str__(self):
        return self.player_id

class P_score(models.Model):
    player_id=models.IntegerField(default=0)

    def __str__(self):
        return self.player_id


class Players(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Player_name= models.CharField(max_length=100,default="guest")
    day_score = models.IntegerField(default=0)
    attemt = models.IntegerField(default=0)
    season_score = models.IntegerField(default=0)
    attended = models.BooleanField(default=False)          
    accuracy = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    percentile = models.FloatField(default=0)
    total_days_of_season =  models.IntegerField(default=0)
    number_of_days_participated =  models.IntegerField(default=0)     #save attemted here
    consecutive_streak =  models.IntegerField(default=0)
    date = models.DateField(("Date"), default=datetime.date.today)

    def __str__(self):
        return self.Player_name


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Quiz_up(models.Model):
    Match = models.CharField(max_length=250)    
    Questions = models.CharField(max_length=250)
    option_A =  models.CharField(max_length=250)
    option_B =  models.CharField(max_length=250)
    option_C =  models.CharField(max_length=250)
    option_D =  models.CharField(max_length=250)
    Right_Answer =  models.CharField(max_length=250)
    quiz_fact =  models.CharField(max_length=250)
    image = models.CharField(max_length=250,null=True)

    def __str__(self):
        return self.Questions

#class user_stats(models.Model):
#    Total_score = models.IntegerField(default=0)
 #   Accuracy = models.IntegerField(default=0)
 #   total_days_participated = models.IntegerField(default=0)
 #   Streak = models.IntegerField(default=0)

 #   def __str__(self):
 #       return self.all()

class PlayerScoreDetail(models.Model):
    player_id = models.IntegerField()
    seasonGame_id = models.CharField(max_length=30)
    obtained_marks = models.IntegerField()
    total_marks = models.IntegerField()
    date = datetime.datetime.now()
    group_id = models.CharField(max_length=50)

    def __str__(self):
        return self.player_id



