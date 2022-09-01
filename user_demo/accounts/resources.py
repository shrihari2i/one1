from .models import Quiz_up
from import_export import resources


class QuizResource(resources.ModelResource):

	class Meta:
		model = Quiz_up
		feilds = ("Match","Questions","option_A","option_B","option_C","option_D","Right_Answer","quiz_fact")