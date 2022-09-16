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
from .models import Players, Quiz_up
from .serializers import PlayersSer, QuizupSerializer, PlayersleadSer, Save_score
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



class QuizupAPI(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    

    def get(self, request,*args,**kwargs):
        user_data = request.data
        print("\n\n\n")
        #a = request.user
        #print(a)
        
        question_count_from_admin=10
        got = {'user':str(request.user.id)}
        content = int(got["user"])
        quiz_send = Quiz_up.objects.order_by('?')[:question_count_from_admin]
        serializer = QuizupSerializer(quiz_send, many=True)
        tobesend = serializer.data
        
        current_datetime = datetime.datetime.now()
        return Response({'success': True, 'message': 'null', "data": {'count': question_count_from_admin, 'next': "null", 'previous': "null","results": tobesend,"server_datetime": current_datetime}})
        

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
        x.attemt = (user_data['attempt'])
        x.save()
        y = Players.objects.get(pk=content)
        serializer = PlayersleadSer(y)
        data = serializer.data
        current_datetime = datetime.datetime.now()
        return Response({'status': True, "data": {'deatils': "Result Send successfully", "results": data, },
                         "server_datetime": current_datetime
                         })
