from dataclasses import fields
from django.contrib.auth.models import User, Group
from rest_framework import serializers
#from user_demo.accounts.views import Score
from .models import Players
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login  
from rest_framework import exceptions
from django.contrib.auth.models import User, Group
#from .models import Quiz_up, PlayerScoreDetail, My_score, P_score, user_stats

from .models import question_bank, player_score, player_stats, GU_Players, select_winners


class GU_PlayersSer(serializers.ModelSerializer):  #playerSe is old name
    class Meta:
        model = GU_Players
        fields = ['Player_name',
                'day_score', 
                'season_score', 
                'attended',
                'accuracy',
                'total_days_of_season',
                'number_of_days_participated',
                'consecutive_streak',
                'date']

class PlayersleadSer(serializers.ModelSerializer):
    class Meta:
        model = GU_Players
        fields = ['id','Player_name',
                'day_score', 
                'season_score',]


class Save_score(serializers.Serializer):
   # class Meta:
    #    model = Players
     #   fields = ['id',
      #         'day_score', 
       #         'number_of_days_participated',]
    #user = serializers.OneToOneField(User, on_delete=models.CASCADE)
    day_score = serializers.IntegerField(default=0)
    number_of_days_participated =  serializers.IntegerField(default=0) 
    def create(self,validate_data):

        return Players.objects.create(**validate_data)


class question_bankSerializer(serializers.ModelSerializer):

    class Meta:
        model = question_bank #Quiz_up
        fields = "__all__"


# class PlayerScoreSerializer(serializers.Serializer):
#     class Meta:
#         model = PlayerScoreDetail
#         fields = '__all__'

# class P_scoreSerializer(serializers.Serializer):
#     class Meta:
#         model = P_score
#         fields = ('player_id')
#     def create(self,validate_data):
#         return P_score.objects.create(**validate_data)

class player_scoreSerializer(serializers.ModelSerializer):#Myscore
    class Meta:
        model = player_score
        fields = ('player_id','myscr','season_gameid','total_score','played_dt','player_groupid')
    def create(self,validate_data):
        return player_score.objects.create(**validate_data)
        
class player_statsSerializer(serializers.ModelSerializer):

    class Meta:
        model = player_stats
        fields = ('player_id','alloted_qid','groupid','gameid','user_days_score', 'user_total_score','marks_of_days_quiz','total_marks_of_quiz','accuracy','total_days_participated','consecutive_streak','date_of_participation')    
    def create(self,validate_data):
        return player_stats.objects.create(**validate_data)

class show_player_statsSerializer(serializers.ModelSerializer):

    class Meta:
        model = player_stats
        fields = ('player_id','alloted_qid','groupid','gameid','user_days_score', 'user_total_score','marks_of_days_quiz','total_marks_of_quiz','accuracy','total_days_participated','consecutive_streak','date_of_participation')    
    def create(self,validate_data):
        return player_stats.objects.create(**validate_data)

class leaderboardSerializer(serializers.ModelSerializer):

    class Meta:
        model = player_stats
        fields = ('player_id','user_days_score', 'user_total_score')    

class select_winnersSerializer(serializers.ModelSerializer):

    class Meta:
        model = select_winners
        fields = ('winner_ids','game_id', 'winner_category','winner_selection_date','winner_selection_range_from','winner_selection_range_to')      