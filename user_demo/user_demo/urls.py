"""user_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from accounts.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quizsendapi/',QuizupAPI.as_view()),
  #  path('showstat', showstat.as_view()),
  #  path('player/',playerdetail.as_view()),
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('api/users/', ListUsers.as_view()),
    path('leaderboard/',leaderboard.as_view()),
  #  path('PlayerScoreDetail/', PlayerScoreDetail.as_view()),
    # path('score/', Score.as_view()),
 #   path('pscore/',P_score.as_view()),
    path('playerscore/',My_score.as_view()),
    path('showplayerstats/',show_player_stats.as_view())
    
   
]
