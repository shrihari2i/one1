from dataclasses import dataclass
from importlib.resources import contents
from multiprocessing.sharedctypes import Value
from tokenize import group
from unittest import result
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
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
#from .models import Players, Quiz_up, PlayerScoreDetail
#from .models import P_score as P_scoreModel
from .models import player_score as player_scoreModel
from .models import player_stats as player_statsModel 
#from .serializers import PlayersSer, QuizupSerializer, PlayersleadSer, Save_score, PlayerScoreSerializer, P_scoreSerializer, My_scoreSerializer, user_statsSerializer
from .models import player_stats,player_score,question_bank, GU_Players, select_winners as select_winnersModel
   
from .serializers import question_bankSerializer, player_scoreSerializer, player_statsSerializer,show_player_statsSerializer,leaderboardSerializer, select_winnersSerializer
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
       # req_player_id = request.data
        #print("\n\n\n")
      #  a = request.user
        #print(a)
    
        question_count_from_admin=10
        duration_ques=60
        marks_of_each_ques=10
        try:

         got = {'user':str(request.user.id)}
         content = int(got["user"])
      #   ques_sort_by_today=question_bank.objects.filter(date_of_ques_in_quiz=date.today())
         quiz_send = question_bank.objects.order_by('?')[:question_count_from_admin]
      #   quiz_send = ques_sort_by_today.order_by('?')[:question_count_from_admin]
         serializer = question_bankSerializer(quiz_send, many=True)
         tobesend = serializer.data
         print(tobesend)
         current_datetime = datetime.datetime.now()
         return Response({'success': True, 'message': 'Success', "data": {'count': question_count_from_admin, 'Duration': duration_ques, 'total_marks': marks_of_each_ques, "results": tobesend}})
        except Exception as e:
            print("QuizsendAPI"+e)
            return Response({'Success': False, 'message': 'Oops!!! Something went wrong. Contact Admin'})   

class CheckIfPlayed(APIView):
     authentication_classes = [authentication.TokenAuthentication, ]
     permission_classes = [permissions.IsAuthenticated, ]
  #   @api_view(['GET'])
    # @permission_classes([AllowAny])
     def get(self, request,*args,**kwargs):
        
        req_data = request.data
        print("Check"+req_data.get('player_id'))   
        print("Check grp"+req_data.get('player_groupid'))   
        
        queryset1 = player_statsModel.objects.all();
        queryset = queryset1.filter(player_id=req_data.get('player_id')) & player_statsModel.objects.filter(date_of_participation=req_data.get('played_dt')) & player_statsModel.objects.filter(groupid=req_data.get('player_groupid'))
        print(queryset.count())
        if (queryset.count()):
            return Response({"Success": False, "message": "You have played the game today. You may play tomorrow"})
     
        else:
            return Response({"Success": True, "message": "Wish you good luck for quiz"})
           
        #print("\n\n\n")
        #  a = request.user
        #print(a)
        

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

    def post(self, request):
        req_data=request.data
        queryset = player_statsModel.objects.all();#filter(gameid=req_data['season_gameid']) & player_statsModel.objects.filter(gameid=req_data['player_groupid']) ### filter must be added for filtering by groupid and gameid
        print(str(req_data.get('ascORdec'))+"  "+req_data['season_gameid']+"  "+req_data['player_groupid'])
     #   print(queryset)
        if req_data.get('ascORdec')==0:
             b  = queryset.order_by('user_days_score')
        elif req_data.get('ascORdec')==1:
             b  = queryset.order_by('-user_days_score')     
        elif req_data.get('ascORdec')==2:
             b  = queryset.order_by('user_total_score')     
        elif req_data.get('ascORdec')==3:
             b  = queryset.order_by('-user_total_score')         
        print(b)
        try:
        # If they need count, next, previous page link then we can implement below code
            paginator = PageNumberPagination()
            result_page = paginator.paginate_queryset(b, request)
            serializer = leaderboardSerializer(result_page, many=True)
            result = paginator.get_paginated_response(serializer.data)
        ### end of pagination code    
            # result = leaderboardSerializer(b, many=True) ## use this line if pagination is not required,
            print(queryset.count())
            ld_strip = queryset.values_list()
            return Response({"Success":True, "Message":"Leaderboard Records","Results":result.data})
        except Exception as e:
            print(e)
            return Response({"Success":False,"Message":"Record not found"})
   
   
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


    def getUser_stats_queryset(self):
        queryset = player_statsModel.objects.all()
        return queryset

    def post(self, request, format=None):
       
        data=request.data
        print(data['player_id'],'############')
        serializer = player_scoreSerializer(data=request.data)  
   ##################################

        serializer1 = player_statsSerializer(data=request.data)
            
        ps_user_data = request.data
        get_id = {'user': str(request.user.id)}
        ps_player_id = (ps_user_data['player_id'])  
        ps_gameid = (ps_user_data['season_gameid'])
        ps_groupid = (ps_user_data['player_groupid'])
        ps_user_days_score = (ps_user_data['myscr'])
        ps_marks_of_days_quiz  = (ps_user_data['total_score'])
        ps_played_dt=(ps_user_data['played_dt'])
        
        df = player_scoreModel.objects.create (player_id= ps_player_id,
                                                season_gameid=ps_gameid,
                                                myscr=ps_user_days_score,
                                                player_groupid=ps_groupid,
                                                total_score=ps_marks_of_days_quiz,
                                                played_dt=ps_played_dt
                                            
                                            ) 
        df.save()
        serializer=player_scoreSerializer(df)
   ###################################
        
     #   if serializer.is_valid():
      #   print("in is valid")   
     #    serializer.create(request.data)  ##########posting the data in player_score tble
          
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

                print("xxxxxxxxxxxxxxxxx",x[0])
                b.update(user_total_score=x[0]+data['myscr'])
                b.update(marks_of_days_quiz=data['total_score'])
                y=b.values_list('total_marks_of_quiz', flat=True)
                b.update(total_marks_of_quiz =y[0]+data['total_score'])  # totalk marks of quiz till date( out of)
                z=b.values_list('accuracy',flat=True)
                print(z[0],'  myscr: ',data['myscr'],'  total score : ',data['total_score'])
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
    ######## LOGIC TO INSERT THE NEW PLAYER ID IN player_STATS TABLE  
                serializer1 = player_statsSerializer(data=request.data)
                #print(" in b=0")
                user_data = request.data
                get_id = {'user': str(request.user.id)}
                player_id = (user_data['player_id'])  
                #print("player id"+player_id)
                player_name=(user_data['player_name'])
                #print("player_name"+player_name)
                alloted_qid = "1,2,2,2" #it is just for provision. currently this is not used on any feature
                gameid = (user_data['season_gameid'])
                groupid = (user_data['player_groupid'])
                #print("1")
                user_days_score = (user_data['myscr'])
                user_total_score=(user_data['myscr'])
                #print("2")
                marks_of_days_quiz  = (user_data['total_score'])
                total_marks_of_quiz = (user_data['total_score'])
                accuracy = ((user_data['myscr'])/(user_data['total_score'])*100)

                #print("c")
                total_days_participated=1
                consecutive_streak=1
                streak_counter=0
                date_of_participation=(user_data['played_dt'])
                profile_photo_url=(user_data['profile_photo_url'])
                print("before query")
                df = player_statsModel.objects.create (player_id= player_id,player_name=player_name,alloted_qid=alloted_qid,gameid=gameid,
                                                    groupid=groupid,user_days_score=user_days_score,
                                                    user_total_score=user_total_score,
                                                    marks_of_days_quiz=marks_of_days_quiz,
                                                    total_marks_of_quiz=total_marks_of_quiz,accuracy=accuracy,
                                                    total_days_participated=total_days_participated,
                                                    consecutive_streak=consecutive_streak,streak_counter=streak_counter,
                                                    date_of_participation=date_of_participation, profile_photo_url=profile_photo_url) 
                
                df.save()
                serializer=player_statsSerializer(df)
                return Response({'Success': True,  "Message":"Record inserted Successfully", "data": {"results": data,
                                } 
                                    })
            except Exception as e:
                print("CCCCCCCCCCC")
                print(e)
                return Response({'Success': False, "Message":"Record not inserted" , "data": {
                               } 
                                    })
##### This API retrieve the data and send to Player statistics
class show_player_stats(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer = show_player_statsSerializer
    serailizer_scr = player_scoreSerializer

    def get_queryset(self):
       queryset = player_statsModel.objects.all()
       queryset = player_stats.objects.order_by('user_days_score')
       print(queryset)
       return queryset


    def post(self, request):
      try:  
       queryset = self.get_queryset()
     #  ha=queryset.order_by("-accuracy")[: :-1]  #get highest accuracy
     #  print(ha,"**********************")
       max1 = queryset.order_by("-accuracy")
       print("^^^^^^^^")
       data=request.data
       print("data")
       req_player_id = data.get("player_id")
       print(req_player_id)
    #   print("################")
       a=max1.values_list('accuracy', flat=True)
    #   print(a[0])
       max2=queryset.filter(player_id = req_player_id)
    
       z=max2.values_list('accuracy',flat=True)
       print("accuracy of: "+req_player_id+" is " +str(z[0]))
       percentile = (z[0]/a[0])*100
       print("percentile: "+str(percentile))
       max3=queryset.order_by("accuracy")
       max_accu = max3.values_list('accuracy',flat=True)
    #   print(max_accu) 
       player_id_list = max3.values_list('player_id',flat=True)
    #   print(player_id_list)
       accu_groupby = queryset.order_by('-accuracy').values('accuracy').distinct()
       max_accu_groupby = accu_groupby.values_list('accuracy',flat=True)
    #   print(max_accu_groupby) 
       index=0
       inner_ind=0
       gb_ind=0
       for player_id in max3.iterator():
        index=index+1
     #   print(str(player_id)+" "+req_player_id)#+" "+max_accu)
        if str(player_id)==req_player_id:
      #      print(" Rank: ",+index)
            inner_ind=index
            break
           
            
       inner_index=0    
       for x in max_accu.iterator():
            inner_index=inner_index+1
            if(inner_index==inner_ind):
                gb_ind=x
     #           print(x)
                break
                
       gb_index=0        
       for y in max_accu_groupby.iterator():
            gb_index=gb_index+1
         #   print(str(y)+"  "+str(x))
            if(y==x):
                print (" RANK: "+str(gb_index))
                break
      
       player_total_score = max2.values_list('user_total_score',flat=True)
       print("player_total_score: "+str(*player_total_score,))
       days_participated = max2.values_list('total_days_participated',flat=True)
       print("days_participated: "+str(*days_participated,))
       streak = max2.values_list('consecutive_streak',flat=True)
       print("streak:"+str(*streak,))
       ############## data from player score to plot graph
       queryset_scr = player_scoreModel.objects.filter(player_id=req_player_id)
       queryset_scr_dt = queryset_scr.order_by('played_dt')
       queryset_player_name = max2.values_list('player_name', flat=True)
       queryset_profile_photo_url = max2.values_list('profile_photo_url', flat=True)
       xy_data = queryset_scr_dt.values('played_dt','myscr') 
      # x_qdt = queryset_scr_dt.values_list('played_dt',flat=True)
       
       print(" player id :"+req_player_id)
      

       ############################# end of graph data code 
        # return Response({'success': True, 'message': 'Success', "data": {'count': question_count_from_admin, 'Duration': duration_ques, 'total_marks': marks_of_each_ques, "results": tobesend}})
        # except:
        #  return Response({'Success': False, 'message': 'Oops!!! Something went wrong. Contact Admin'})   

       serializer = show_player_statsSerializer(queryset,many=True)
       return Response({'success': True, 'message': 'Success', "data": {'player_total_score': str(*player_total_score)
                                    , 'Accuracy': str(z[0])+'%', 'Rank': gb_index, "percentile": percentile,'total_days_of_the_season':50,
                                    'no.of_days_participated': str(*days_participated),'streak':str(*streak,) ,'player_name':queryset_player_name[0],'profile_photo_url':queryset_profile_photo_url[0], 'bar_chart':xy_data}})
      except Exception as e: 
        print(e)
        return Response({'success': False, 'message': 'Error!', "data": { }})
      
    # def post(self, request, format=None):
       
    #   #  print(request.data,'############')
    #     serializer = player_statsSerializer(data=request.data)
    #     if serializer.is_valid():
    #   #      print(request.data,'###################')
    #         serializer.create(request.data)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class select_winners(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer = select_winnersSerializer
    
    def post(self, request):
        req_data = request.data;
        req_player_id = req_data.get('player_id')
        req_game_id = req_data.get('season_gameid')
        req_group_id=req_data.get('player_groupid')
        req_winner_category = req_data.get('winner_category')
        req_winner_selection_date = req_data.get('winner_selection_date')
        req_winner_selection_range_from = req_data.get('winner_selection_range_from')
        req_winner_selection_range_to = req_data.get('winner_selection_range_to')
        print(req_group_id)
        print(req_game_id)
        print(req_winner_selection_range_from)
        print(req_winner_selection_range_to)
        try:
      
            queryset = player_statsModel.objects.all();#filter(groupid=req_group_id) & player_statsModel.objects.filter(gameid=req_game_id) # & player_statsModel.objects.filter(date_of_participation__range=[req_winner_selection_range_from, req_winner_selection_range_to]) 
            
            print(queryset)
            select_random=queryset.order_by('?')[:3]
            selected_winners=select_random.values_list('player_id', flat=True)
            selected_winner_str=selected_winners[0]+","+selected_winners[1]+","+selected_winners[2]
            ############## Below code is inserting data in #######################
            df = select_winnersModel.objects.create (winner_ids= selected_winner_str, game_id=req_game_id,
                                                    winner_category=req_winner_category, winner_selection_date=req_winner_selection_date,
                                                    winner_selection_range_from=req_winner_selection_range_from,
                                                    winner_selection_range_to=req_winner_selection_range_to
                                                    
                                              ) 
            df.save()
           # serializer=select_winnersSerializer(df)
          #  serializer=player_statsSerializer(select_random)
            print("&&&&&&&&&&&&")
            return Response({'success':True, 'message': "Randomly selected 3 winner"})#, "data":{serializer.data}})
        except Exception as e:
                print(e)
                return Response({'success':False, 'message': "Oops!! somthing wrong"})
            ######################################

        #  serializer = select_winnersSerializer(select_random,many=True)
            # return Response({'success':True, 'message': "Randomly selected 3 winner"})# "data":{serializer.data}})
            # except:
            #     return Response({'success':False, 'message': "Oops!! somthing wrong"})

class leaderboard_strip(APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]
   

    def post(self, request):
        req_data=request.data
        try:  
            queryset = player_statsModel.objects.all()#filter(gameid=req_data['season_gameid']) & player_statsModel.objects.filter(gameid=req_data['player_groupid']) ### filter must be added for filtering by groupid and gameid
            player_id=req_data['player_id']
            print(player_id)
            queryset_user_total_score = queryset.order_by('-user_total_score')
            
        # print(queryset.count())
            vlist_user_total_score = queryset_user_total_score.values_list('user_total_score',flat=True)
            vlist_player_id = queryset_user_total_score.values_list('user_total_score',flat=True)
            
            vlist_player_id =queryset_user_total_score.values_list('player_id',flat=True)
            vlist_player_name =queryset_user_total_score.values_list('player_name',flat=True)
            
            # print(vlist_user_total_score)
            # print(vlist_player_id)
            list_user_total_score = (list(vlist_user_total_score))
            set_user_total_score = list(set(list_user_total_score))
            list_player_id = list(vlist_player_id)
            sorted_set = sorted(set_user_total_score, reverse=True) 
            # print(sorted_set)
            # print(list_player_id )
            index_val = list_player_id.index(player_id)
            # print(index_val+1)
            index_score = list_user_total_score[index_val]
        # print(index_score)
            player_name=vlist_player_name[index_val]
            rank = sorted_set.index(index_score)
            rank=rank+1 #adding one as index starts from 0
            total_player = queryset.count()
            player_score=index_score
            people_behind_player = 100-((rank/total_player)*100)
            print(rank+1)  # Rank
            print(total_player) #total player playing the game
            print(player_score)  # score of the player
            print(player_name) #player name
            print(people_behind_player)
            return Response({'success': True, 'message': 'Success', "data": {'rank': rank, 'total_player':total_player
                                        , 'player_score': player_score, 'player_name': player_name
                                        , "people_behind_player": str(round(people_behind_player))+"%"}})
        except Exception as e:
            print(e)
            return Response({'success':False, 'message':"Something went wrong in strip data"})




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

