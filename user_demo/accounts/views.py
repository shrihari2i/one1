from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.http import HttpResponse
from .models import Players, Quiz_up
from .serializers import PlayersSer, QuizupSerializer,PlayersleadSer,Save_score
import random
import io
from rest_framework.parsers import JSONParser
import json







# acces data after authentication
class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    print(permission_classes)
    def get(self, request, format=None):
    	content= {
    	'user': str(request.user) 
    	}
    	print("\n\n")
    	print(content)
    	return(content)


class showstat(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    print("from show ")
    def get(self, request, format=None):
        got= {'user': str(request.user.id)}            #id fetch
        content= int(got["user"]) 
        print(content)
        u= Players.objects.get(pk=content)
        serializer=PlayersSer(u)
        return Response(serializer.data)
        #return Response(content)



# genarated tokens
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class QuizupAPI(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        q_count= Quiz_up.objects.all().count()
        print(q_count)
        qlist=[]
        while len(qlist) != 5:
            random_number = random.randint(1,q_count)
            if random_number not in qlist:
                qlist.append(random_number)
        print(qlist)
        quiz_send=Quiz_up.objects.filter(id__in = qlist)
        serializer=QuizupSerializer(quiz_send,many=True)
        print("\n\n\n")
        hello = serializer.data
        print(type(hello))
        return Response(serializer.data)

class playerdetail(APIView):
    def get(self,request):
        u= Players.objects.get(pk=1)
        content= {'user': str(request.user)}
        a= content['user']
        print(a)

        serializer=PlayersSer(u)
        return Response(serializer.data)

class leaderboard(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        b=Players.objects.order_by('-day_score')[:5]
        serializer=PlayersleadSer(b,many=True)
        return Response(serializer.data)




class Score(APIView):

   # authentication_classes = [authentication.TokenAuthentication]
   
   # permission_classes = [permissions.IsAuthenticated]


    def players_create(request):
        if request.method == "POST":
            json_data = json.loads(request.Body)
            stream = io.BytesIO(json_data)
            python_data = JSONParser().parse(stream)
            serializer = Save_score(data=python_data)
            if serializer.is_valid():
                serializer.save()
                result = {'msg' : 'Data created'}
                json_data = JSONRenderer().render(res) 
                return HttpRespose(json_data, content_type='application/json')




'''
class Score(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def put(self,request):
         
        print("from show ")
        ds= ['headers'][days]
        def get(self, request, format=None):
        got= {'user': str(request.user.id)}
        content= int(got["user"]) 
        print(content)
        u= Players.objects.get(pk=content)
        u.day_score=ds
        u.save()
        serializer=PlayersSer(u)


'''
'''
class save_score(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        i = request.Body['User_id']
        i = request.Body['Score']
        i = request.Body['attempt']
        u = request

        x = request.data()
        u = Players.objects.get(pk=id)
        print(request.data)
'''


