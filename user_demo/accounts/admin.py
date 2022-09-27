from dataclasses import fields
from django.contrib import admin
from .models import GU_Players, question_bank, player_stats #PlayerScoreDetail, Quiz_up, user_stats
from .models import question_bank
from import_export.admin import ImportExportModelAdmin
# Register your models here.

admin.site.register(GU_Players) #(Players) was old model


@admin.register(question_bank)  #Quiz_up was old model
class QuizAdmin(ImportExportModelAdmin):
	exclude = ('id',)
# @admin.register(PlayerScoreDetail)
# class PlayerScoreDetailAdmin(admin.ModelAdmin):
# 	fields = ('player_id','seasonGame_id','obtained_marks','total_marks','group_id')

@admin.register(player_stats)
class user_statsAdmin(admin.ModelAdmin):
   	fields = ('player_id','alloted_qid','groupid','gameid','user_days_score','user_total_score','marks_of_days_quiz','total_marks_of_quiz','accuracy','total_days_participated','consecutive_streak', 'streak_counter','date_of_participation')




	