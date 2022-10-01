from email.policy import default
from django.utils import timezone
from tkinter.tix import Tree
from django.db import models
from django.contrib.auth.models import User
import datetime
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from datetime import date
# Create your models here.

class ques_list(models.Model):
    qid=models.CharField(max_length=10)
    ques=models.CharField(max_length=550)
    def __str__(self):
        return self.Questions 



class Quiz_up(models.Model):
    Match = models.CharField(max_length=250)    
    Questions = models.CharField(max_length=250)
    option_A =  models.CharField(max_length=250)
    option_B =  models.CharField(max_length=250)
    option_C =  models.CharField(max_length=250)
    option_D =  models.CharField(max_length=250)
    Right_Answer =  models.CharField(max_length=250)
    quiz_fact =  models.CharField(max_length=250)
    image = models.ImageField(default="logo.png")

    def __str__(self):
        return self.Questions

class My_score(models.Model):
    player_id=models.CharField(max_length=10,default = 'player_id') 
    myscr = models.IntegerField(default=0)  
    season_gameid = models.CharField(max_length=10,default='gameid') 
    total_score = models.IntegerField(default=0)
    played_dt = models.DateField(date.today()) #models.CharField(max_length=15, default='1/1/2022')
    player_groupid = models.CharField(max_length=10,default='group_id')

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
        Token.objects.create(user=instance)

# class Quiz_up(models.Model):
#     Match = models.CharField(max_length=250)    
#     Questions = models.CharField(max_length=250)
#     option_A =  models.CharField(max_length=250)
#     option_B =  models.CharField(max_length=250)
#     option_C =  models.CharField(max_length=250)
#     option_D =  models.CharField(max_length=250)
#     Right_Answer =  models.CharField(max_length=250)
#     quiz_fact =  models.CharField(max_length=250)
#     image = models.ImageField(default="logo.png")

#     def __str__(self):
#         return self.Questions

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

class user_stats(models.Model):

    player_id=models.CharField(max_length=10) #models.OneToOneField(User, on_delete=models.CASCADE)
    alloted_qid=models.CharField(max_length=100)
    groupid = models.CharField(max_length=10) #groupis
    gameid = models.CharField(max_length=10) #gameid
    user_days_score=models.IntegerField(default=10) #user_score
    user_total_score=models.IntegerField(default=0)
    marks_of_days_quiz=models.IntegerField(default=0) #score from out of marks day's 
    total_marks_of_quiz=models.IntegerField(default=0) # totalk marks of quiz till date( out of)
    accuracy=models.IntegerField(default=0)
    total_days_participated=models.IntegerField(default=0)
    consecutive_streak =  models.IntegerField(default=0)
    streak_counter = models.IntegerField(default=0)
    date_of_participation = models.DateField(default=date.today())  #dats
    
    def __str__(self):
        return self.player_id
######################  New Models
class player_stats(models.Model):   ####  old name user_stats

    player_id=models.CharField(max_length=10) #models.OneToOneField(User, on_delete=models.CASCADE)
    player_name=models.CharField(max_length=50, default="Not Available")
    alloted_qid=models.CharField(max_length=100)
    groupid = models.CharField(max_length=10) #groupis
    gameid = models.CharField(max_length=10) #gameid
    user_days_score=models.IntegerField(default=10) #user_score
    user_total_score=models.IntegerField(default=0)
    marks_of_days_quiz=models.IntegerField(default=0) #score from out of marks day's 
    total_marks_of_quiz=models.IntegerField(default=0) # totalk marks of quiz till date( out of)
    accuracy=models.IntegerField(default=0)
    total_days_participated=models.IntegerField(default=0)
    consecutive_streak =  models.IntegerField(default=0)
    streak_counter = models.IntegerField(default=0)
    date_of_participation = models.DateField(default=date.today())  #dats
    profile_photo_url = models.CharField(max_length=100, default="Not Available")
    
    def __str__(self):
        return self.player_id

class GU_Players(models.Model):  #### old name player
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
        s
class player_score(models.Model):   ## old name My_score
    player_id=models.CharField(max_length=10,default = 'player_id') 
    myscr = models.IntegerField(default=0)  
    season_gameid = models.CharField(max_length=10,default='gameid') 
    total_score = models.IntegerField(default=0)
    played_dt = models.DateField(date.today()) #models.CharField(max_length=15, default='1/1/2022')
    player_groupid = models.CharField(max_length=10,default='group_id')

    def __str__(self):
            return self.player_id

class question_bank(models.Model):   ######### old name quiz_up
    Match = models.CharField(max_length=250)    
    Questions = models.CharField(max_length=250)
    option_A =  models.CharField(max_length=250)
    option_B =  models.CharField(max_length=250)
    option_C =  models.CharField(max_length=250)
    option_D =  models.CharField(max_length=250)
    Right_Answer =  models.CharField(max_length=250)
    quiz_fact =  models.CharField(max_length=250)
    image = models.ImageField(default="logo.png")
 #   date_of_ques_in_quiz=models.DateField(default="2022-12-01")

    def __str__(self):
        return self.Questions            

class select_winners(models.Model):
    winner_ids=models.CharField(max_length=250)
    game_id = models.CharField(max_length=10)
    winner_category = models.CharField(max_length=10)
    winner_selection_date = models.DateField(default="2022,12-24")
    winner_selection_range_from=models.DateField(default="2022-12-34")
    winner_selection_range_to=models.DateField(default="2022-12-34")

    def __str__(self):
        return self.player_id