from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Players
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login  
from rest_framework import exceptions
from django.contrib.auth.models import User, Group
from .models import Quiz_up


class PlayersSer(serializers.ModelSerializer):
    class Meta:
        model = Players
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
        model = Players
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


class QuizupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quiz_up
        fields = "__all__"


        




