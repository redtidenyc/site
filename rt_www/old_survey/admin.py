from django.contrib import admin

from old_survey.models import *

class SurveyAdmin(admin.ModelAdmin):
    pass
admin.site.register(Survey, SurveyAdmin)

class QuestionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Question, QuestionAdmin)

class QuestionPlaceAdmin(admin.ModelAdmin):
    pass
admin.site.register(QuestionPlace, QuestionPlaceAdmin)

class SwimmerToSurveyAdmin(admin.ModelAdmin):
    list_display = ('swimmer', 'survey',)
    list_filter = ('survey',)
    search_fields = ('swimmer__user__first_name', 'swimmer__user__last_name', )
admin.site.register(SwimmerToSurvey, SwimmerToSurveyAdmin)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', )
    list_filter = ('survey', )
admin.site.register(Answer, AnswerAdmin)