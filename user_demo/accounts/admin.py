from dataclasses import fields
from django.contrib import admin
from .models import Players, PlayerScoreDetail
from .models import Quiz_up
from import_export.admin import ImportExportModelAdmin
# Register your models here.

admin.site.register(Players)


@admin.register(Quiz_up)
class QuizAdmin(ImportExportModelAdmin):
	exclude = ('id',)
@admin.register(PlayerScoreDetail)
class PlayerScoreDetailAdmin(admin.ModelAdmin):
	fields = ('player_id','seasonGame_id','obtained_marks','total_marks','group_id')