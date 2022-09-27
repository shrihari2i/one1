from importlib.resources import contents
from tokenize import group
from django.shortcuts import render
from datetime import date
from datetime import datetime

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
#from .models import Players, Quiz_up, PlayerScoreDetail
#from .models import P_score as P_scoreModel
from .models import player_score as player_scoreModel
from .models import player_stats as player_statsModel 
#from .serializers import PlayersSer, QuizupSerializer, PlayersleadSer, Save_score, PlayerScoreSerializer, P_scoreSerializer, My_scoreSerializer, user_statsSerializer
from .models import player_stats,player_score,question_bank, GU_Players
from .serializers import question_bankSerializer, player_scoreSerializer, player_statsSerializer,show_player_statsSerializer
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
    

    def get(self, request, format=None):
        content = {
            'user': str(request.user)
        }
        print("\n\n")
        print(content)
        return (content)


# class showstat(ListAPIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
   

#     def get(self, request, format=None):
#         got = {'user': str(request.user.id)}  # id fetch
#         content = int(got["user"])
#         print(content)
#         u = Players.objects.get(pk=content)
#         serializer = PlayersSer(u)
#         return Response(serializer.data)


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


### for fetching questions **************************************
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
        marks_of_each_ques=10
        try:

         got = {'user':str(request.user.id)}
         content = int(got["user"])
         quiz_send = question_bank.objects.order_by('?')[:question_count_from_admin]
         serializer = question_bankSerializer(quiz_send, many=True)
         tobesend = serializer.data
         current_datetime = datetime.datetime.now()
         return Response({'success': True, 'message': 'Success', "data": {'count': question_count_from_admin, 'Duration': duration_ques, 'total_marks': marks_of_each_ques, "results": tobesend}})
        except:
         return Response({'Success': False, 'message': 'Oops!!! Something went wrong. Contact Admin'})   
#### fetch question end ********************************************
# class playerdetail(ListAPIView):
#     def get(self, request):
#         u = Players.objects.get(pk=1)
#         content = {'user': str(request.user)}
#         a = content['user']
#         print(a)

#         serializer = PlayersSer(u)
#         return Response(serializer.data)


class leaderboard(APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]
    pagination_class = PageNumberPagination

    def get(self, request):
        my_scoredata=request.data
        queryset = player_scoreModel.objects.all()
      #  queryset = My_scoreModel.objects.filter(player_id=100)
      #  print(queryset.get('myscr'),'*****************************')
      #  b = queryset.order_by('-day_score')
        b = queryset.filter(player_id=my_scoredata.get('player_id')) & queryset.filter(player_groupid=my_scoredata.get('groupid'))
        x=b.values_list('myscr', flat=True)
        print(x[0])
        b.update(myscr=14)
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(b, request)
        serializer = PlayersleadSer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

## on submit questions
# class Score(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         print('\n\n')
#         user_data = request.data
#         got = {'user': str(request.user.id)}
#         content = int(got["user"])
#         print(content)
#         x = Players.objects.get(pk=content)
#         x.day_score = (user_data['Score'])
#         x.attemt = (user_data['attemt'])
#         x.save()
#         y = Players.objects.get(pk=content)
#         serializer = PlayersleadSer(y)
#         data = serializer.data
#         current_datetime = datetime.datetime.now()
#         return Response({'status': True, "data": {'deatils': "Result Send successfully", "results": data, },
#                          "server_datetime": current_datetime
 
#                          })


# ### by Kishore
# class PlayerScoreDetail(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = PlayerScoreSerializer

#     def post(self, request, *args, **kwargs):
#         user_data = request.data
#         get_id = {'user': str(request.user.id)}
#         player_id = int(get_id["user"])
#         obj = PlayerScoreDetail.objects.get(pk=player_id)
#         obj.player_id = player_id
#         obj.season_gameid = (user_data['season_gameid'])
#         obj.obtained_marks = (user_data['obtained_marks'])
#         obj.total_marks  = (user_data['total_marks'])
#         obj.group_id = (user_data['group_id'])
#         obj.accuracy = obtai
#         obj.save()
#         playerdata = PlayerScoreDetail.objects.get(pk=player_id)
#         serializer = PlayerScoreSerializer(playerdata)
        
#         return Response(data = serializer.data)
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

# class P_score(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request, format=None):
#         serializer = P_scoreSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# This API save the data in My_score table when player submit the quiz.
class My_score(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

   # def get(self, request, format=None):
   #     table_data = My_scoreModel.objects.all()
   #     print(table_data.query,'___________________________________')
   #     serializer = My_scoreSerializer(table_data, many=True)
   #     return Response(serializer.data)
    def getUser_stats_queryset(self):
        queryset = player_statsModel.objects.all()
        return queryset

    def post(self, request, format=None):
       
        data=request.data
        print(data['player_id'],'############')
        serializer = player_scoreSerializer(data=request.data)
   
        
        if serializer.is_valid():
         print("in is valid")   
         serializer.create(request.data)
          
        queryset1=self.getUser_stats_queryset()
      #  print("************",queryset1.values('alloted_qid'))
      #  print("player   ",data.get('player_id'))
      #  print("groupid   ",data.get('player_groupid'))
      #  print("gameid   ",data.get('season_gameid'))
        b = queryset1.filter(player_id=data.get('player_id')) & queryset1.filter(groupid=data.get('player_groupid')) & queryset1.filter(gameid=data.get('season_gameid'))
        pid=b.values_list('player_id',flat=True)
        print("++++++++", b.count())

        if b.count()>0:
            try:
       # b.update(user_days_score=data['myscr'])
                x=b.values_list('user_total_score', flat=True)

        #  print("xxxxxxxxxxxxxxxxx",x[0])
                b.update(user_total_score=x[0]+data['myscr'])
                b.update(marks_of_days_quiz=data['total_score'])
                y=b.values_list('total_marks_of_quiz', flat=True)
                b.update(total_marks_of_quiz =y[0]+data['total_score'])  # totalk marks of quiz till date( out of)
                z=b.values_list('accuracy',flat=True)
        #  print(z[0],'  myscr: ',data['myscr'],'  total score : ',data['total_score'])
                b.update(accuracy=((z[0]+(data['myscr']/data['total_score'])*100)/2))
                a=b.values_list('total_days_participated',flat=True)
                b.update(total_days_participated=a[0]+1)
        #####LOGIC FOR STREAK########
                scdb=b.values_list('streak_counter', flat=True)
                csdb=b.values_list('consecutive_streak', flat=True)
                streak_counter_db = scdb[0]
                consecutive_streak_db = csdb[0]
                dpdb= b.values_list('date_of_participation',flat=True)
                d={'dt':str(dpdb[0])}
                date_of_participation_DB = datetime.datetime.strptime(d['dt'],"%Y-%m-%d")
                date_of_participation_RQ = datetime.datetime.strptime(data['played_dt'],"%Y-%m-%d")
                delta = date_of_participation_RQ.day -date_of_participation_DB.day

                print("Delta of dates",delta)
                if delta == 1:
                    if consecutive_streak_db < streak_counter_db:
                        b.update(streak_counter=streak_counter_db+1)
                
                    # no change in streak
                        print("first if")
                    elif consecutive_streak_db == streak_counter_db:
                        b.update(consecutive_streak=consecutive_streak_db+1)
                        b.update(streak_counter=0)  
                        print("first elseif")  
                    elif consecutive_streak_db > streak_counter_db:   #
                        if(streak_counter_db==0):
                            b.update(consecutive_streak=consecutive_streak_db+1)
                            print("iiner if")
                        else:
                            b.update(streak_counter=streak_counter_db+1)  
                            print("inner else")          
                            # No change in counter
                            print("second else if")
                    else:
                        b.update(streak_counter=1)          
                # no change in streak  
                    print("last else if")      
        

        #####END OF STREAK LOGIC#########
                #  b.update(consecutive_streak =  models.IntegerField(default=0))
                b.update(date_of_participation = data['played_dt'])
                data = serializer.data
                return Response({'Success': True, "Message":"Record updated Successfully","data": {"results": data,
                                 } 
                                    })
            except:
                return Response({'Success': False,"Message":"Record not updated", "data": {
                                 } 
                                    })
        elif b.count()==0:
            try:
    ######## LOGIC TO INSERT THE NEW PLAYER ID IN USER_STATS TABLE  
                serializer1 = player_statsSerializer(data=request.data)
            
                user_data = request.data
                get_id = {'user': str(request.user.id)}
                player_id = (user_data['player_id'])  
                alloted_qid = "1,2,2,2"
                gameid = (user_data['season_gameid'])
                groupid = (user_data['player_groupid'])
                user_days_score = (user_data['myscr'])
                user_total_score=(user_data['myscr'])
                marks_of_days_quiz  = (user_data['total_score'])
                total_marks_of_quiz = (user_data['total_score'])
                accuracy = ((user_data['myscr'])/(user_data['total_score'])*100)
                total_days_participated=1
                consecutive_streak=1
                streak_counter=0
                date_of_participation=(user_data['played_dt'])
            
                df = player_statsModel.objects.create (player_id= player_id,alloted_qid=alloted_qid,gameid=gameid,
                                                    groupid=groupid,user_days_score=user_days_score,
                                                    user_total_score=user_total_score,
                                                    marks_of_days_quiz=marks_of_days_quiz,
                                                    total_marks_of_quiz=total_marks_of_quiz,accuracy=accuracy,
                                                    total_days_participated=total_days_participated,
                                                    consecutive_streak=consecutive_streak,streak_counter=streak_counter,
                                                    date_of_participation=date_of_participation) 
                df.save()
                serializer=player_statsSerializer(df)
                return Response({'Success': True,  "Message":"Record inserted Successfully", "data": {"results": data,
                                } 
                                    })
            except:
                return Response({'Success': False, "Message":"Record not inserted" , "data": {
                               } 
                                    })
##### This API retrieve the data and send to Player statistics
class show_player_stats(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer = show_player_statsSerializer

    def get_queryset(self):
       queryset = player_statsModel.objects.all()
     #  queryset = player_stats.objects.order_by('user_days_score')
       return queryset


    def get(self, request):
       queryset = self.get_queryset()
       max1=queryset.order_by("-accuracy")[0]  #get highest accuracy
       data=request.data
       req_player_id = data.get('player_id')
       print(req_player_id);
       highest_accu = max1.accuracy;
       print(highest_accu)
       max2=queryset.filter(player_id = req_player_id)
     
       z=max2.values_list('accuracy',flat=True)
       percentile = (z[0]/highest_accu)*100
       print("percentile: "+str(percentile))
       max3=queryset.order_by("accuracy")
       print(max3)
    #    index=0
    #    for player_id in max3.iterator():
    #     index=index+1
    #     print(max3.player_id+" "+req_player_id)
    #     if (player_id==req_player_id):
    #         print(" Rank: "+index)
       serializer = show_player_statsSerializer(queryset,many=True)
       return Response(serializer.data)
    
    def post(self, request, format=None):
       
      #  print(request.data,'############')
        serializer = player_statsSerializer(data=request.data)
        if serializer.is_valid():
      #      print(request.data,'###################')
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


