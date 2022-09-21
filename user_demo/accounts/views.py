from importlib.resources import contents
from tokenize import group
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.http import HttpResponse
from .models import Players, Quiz_up, PlayerScoreDetail
from .models import P_score as P_scoreModel
from .models import My_score as My_scoreModel
from .serializers import PlayersSer, QuizupSerializer, PlayersleadSer, Save_score, PlayerScoreSerializer, P_scoreSerializer, My_scoreSerializer

import random
import io
from rest_framework.parsers import JSONParser
import json
from rest_framework.decorators import api_view
from rest_framework import status
from .mypagination import LargeResultsSetPagination, PageNumberPagination
import datetime





# acces data after authentication
class ListUsers(ListAPIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    print(permission_classes)

    def get(self, request, format=None):
        content = {
            'user': str(request.user)
        }
        print("\n\n")
        print(content)
        return (content)


class showstat(ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    print("from show ")

    def get(self, request, format=None):
        got = {'user': str(request.user.id)}  # id fetch
        content = int(got["user"])
        print(content)
        u = Players.objects.get(pk=content)
        serializer = PlayersSer(u)
        return Response(serializer.data)


# genarated tokens
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        a=serializer.is_valid()
        print(a)
        if a==True:
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            user_name = user.username
            serializer = self.get_serializer(data=request.data)
            return Response({'success': True, 'message':"User exists","data": {'token': token.key,'user_id': user.pk,'email': user.email}})
        else:
            return Response({'success': False, 'message':"User does not exist","data": {}})


### for fetching questions 
class QuizupAPI(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    

    def get(self, request,*args,**kwargs):
        user_data = request.data
        #print("\n\n\n")
        #a = request.user
        #print(a)
        
        question_count_from_admin=10
        duration_ques=60
        try:
         got = {'user':str(request.user.id)}
         content = int(got["user"])
         quiz_send = Quiz_up.objects.order_by('?')[:question_count_from_admin]
         serializer = QuizupSerializer(quiz_send, many=True)
         tobesend = serializer.data
         current_datetime = datetime.datetime.now()
         return Response({'success': True, 'message': 'Success', "data": {'count': question_count_from_admin, 'Duration': duration_ques, "results": tobesend}})
        except:
         return Respose({'Success': False, 'message': 'Oops!!! Something went wrong. Contact Admin'})   

class playerdetail(ListAPIView):
    def get(self, request):
        u = Players.objects.get(pk=1)
        content = {'user': str(request.user)}
        a = content['user']
        print(a)

        serializer = PlayersSer(u)
        return Response(serializer.data)


class leaderboard(APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]
    pagination_class = PageNumberPagination

    def get(self, request):
        queryset = Players.objects.all()
        b = queryset.order_by('-day_score')
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(b, request)
        serializer = PlayersleadSer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

## on submit questions
class Score(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print('\n\n')
        user_data = request.data
        got = {'user': str(request.user.id)}
        content = int(got["user"])
        print(content)
        x = Players.objects.get(pk=content)
        x.day_score = (user_data['Score'])
        x.attemt = (user_data['attemt'])
        x.save()
        y = Players.objects.get(pk=content)
        serializer = PlayersleadSer(y)
        data = serializer.data
        current_datetime = datetime.datetime.now()
        return Response({'status': True, "data": {'deatils': "Result Send successfully", "results": data, },
                         "server_datetime": current_datetime
 
                         })


### by Kishore
class PlayerScoreDetail(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PlayerScoreSerializer

    def post(self, request, *args, **kwargs):
        user_data = request.data
        get_id = {'user': str(request.user.id)}
        player_id = int(get_id["user"])
        obj = PlayerScoreDetail.objects.get(pk=player_id)
        obj.player_id = player_id
        obj.season_gameid = (user_data['season_gameid'])
        obj.obtained_marks = (user_data['obtained_marks'])
        obj.total_marks  = (user_data['total_marks'])
        obj.group_id = (user_data['group_id'])
        obj.save()
        playerdata = PlayerScoreDetail.objects.get(pk=player_id)
        serializer = PlayerScoreSerializer(playerdata)
        
        return Response(data = serializer.data)
# End of kishore code

# class P_score(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = P_scoreSerializer
#     def post(self, request, *args, **kwargs):
#          user_data = request.data['player_id']
#          print(user_data,'**********************')
#          get_id = {'user': str(request.user.id)}
#         #id = int(get_id["user"])
#          obj = P_scoreModel.objects.all()
#          obj.id = int(user_data)
         
#          print(obj.id)
#        #  try:
#       #    obj.save()
#       #   except: 
#       #    print('error')
#          pdata = P_scoreModel.objects.all()
#          serializer = P_scoreSerializer(obj)
#          return Response(data = serializer.data)

class P_score(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = P_scoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class My_score(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        table_data = My_scoreModel.objects.all()
        print(table_data.query,'___________________________________')
        serializer = My_scoreSerializer(table_data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = My_scoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)














        # id = user_data.id
        # season_gameid = user_data.season_gameid
        # obtained_marks = user_data.obtained_marks
        # total_marks = user_data.total_marks
        # group_id = user_data.group_id

        # if PlayerScore.objects.get(pk=id):
        #     data = PlayerScore.objects.all()
        #     data.player_id = id
        #     data.season_gameid = season_gameid
        #     data.total_marks = total_marks
        #     data.group_id = group_id
        #     data.obtained_marks = obtained_marks
        #     data.save()
        #     playerdata = PlayerScore.objects.get(pk=id)
        #     serializer = PlayerScoreSerializer(playerdata)
        #     data = serializer.data
        #     return Response({'status':True})


