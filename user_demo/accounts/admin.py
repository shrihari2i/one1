from django.contrib import admin
from .models import Players
from .models import Quiz_up
from import_export.admin import ImportExportModelAdmin
# Register your models here.

admin.site.register(Players)


@admin.register(Quiz_up)
class QuizAdmin(ImportExportModelAdmin):
	exclude = ('id',)