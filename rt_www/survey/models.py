from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.loader import get_template
from django.template import Context, Template
from rt_www.swimmers.models import Swimmer
from django.contrib.sites.models import Site
from django.conf import settings
import cPickle as pickle
import base64

class QuestionType:
    def save_choice_config(self, new_data):
        pass
    def create_choice_widget(self): #This will *always* return a straight hash for JSON dump...formatting handled by javascript
	pass
    def get_edit_hash(self):
        pass
    def render(self):
        pass

class Choice(QuestionType):
    layout_type = ((0, "Horizontal"), (1, "Vertical"), (2, "Menu"),)
    def __init__(self):
        self.layout = 1
	self.choices = {}
	self.append_comments = False 
    def add_choice(self, choice):
	self.choices[choice] = { 'has_comment':0, 'position':len(self.choices.keys()) + 1 }
    def set_append_comments(self, choice):
	try:
	    if self.choices[choice] == 0:
	        self.choices[choice] = 1
	except KeyError:
	    raise KeyError('Choice %s not set' % choice)
    def create_choice_widget(self):
        return {'type':'choice', 'multiple':'0', 'typeid':'0'}
    def save_choice_config(self, new_data):
	counter = 0
	while True:
	    try:
		choice = new_data['choice_%d' % counter]
		has_comment = 0;
		if new_data['checkedchoice_%d' % counter ] == 'on':
		    has_comment = 1
		self.choices[choice] = { 'position':counter, 'has_comment':has_comment }
		counter += 1
	    except KeyError, e:
                break
    def get_edit_hash(self):
	ret_val = self.create_choice_widget()
	choices = [ {'choice':'', 'is_comment':0 } for i in range(len(self.choices.keys())) ]
	for k, v in self.choices.items():
	    choices[v['position']] = { 'choice':k, 'has_comment':v['has_comment'] }
	ret_val['choices'] = choices
	return ret_val
    def render(self):
	choices = [ {'choice':'', 'is_comment':0 } for i in range(len(self.choices.keys())) ]
	for k, v in self.choices.items():
	    choices[v['position']] = { 'choice':k, 'has_comment':v['has_comment'] }
	return {'choices':choices, 'multiple':'0'}

class MultipleAnswerChoice(Choice):
    def create_choice_widget(self):
        return {'type':'choice', 'multiple':'1', 'typeid':'1'}
    def render(self):
        choices = [ {'choice':'', 'is_comment':0 } for i in range(len(self.choices.keys())) ]
	for k, v in self.choices.items():
	    choices[v['position']] = { 'choice':k, 'position':v['position'], 'has_comment':v['has_comment'] }
        return {'choices':choices, 'multiple':'1'}

class Matrix(QuestionType):
    def __init__(self):
        self.row_labels = [] #These are the choices
        self.column_labels = [] #These are the ratings
    def set_row_labels(self, labels):
        self.row_labels = labels
    def set_column_labels(self, labels):
        self.column_labels = labels
    def save_choice_config(self, new_data):
        i = 0
        while True:
            try:
	        self.column_labels.append(new_data['clabel%d' % i])
		i += 1
	    except KeyError:
		break
        i = 0
        while True:
	    try:
	        self.row_labels.append(new_data['rlabel%d' % i])
	        i += 1
	    except KeyError:
	        break

    def create_choice_widget(self):
        return {'type':'matrix', 'typeid':'2'}
	
    def get_edit_hash(self):
        ret_val = self.create_choice_widget()
	ret_val['rows'] = self.row_labels
	ret_val['cols'] = self.column_labels
	return ret_val
	
    def render(self):
	return { 'clabels':self.column_labels, 'rlabels':self.row_labels }

class Comment(QuestionType):
    def create_choice_widget(self):
        return {'type':'comment', 'typeid':'3'}
    def get_edit_hash(self):
        return self.create_choice_widget()
    def render(self):
        return {}

"""
	The create survey dialog is going to be slightly complicated
	basically there needs to be a create Question
"""

QTYPES = (
    (0, 'Choice'),
    (1, 'MultipleAnswerChoice'),
    (2, 'Matrix'),
    (3, 'Comment'),
)

class Question(models.Model):
    question = models.TextField(_('Question Text'))
    question_type = models.IntegerField(_('Question Types'), choices=QTYPES)
    question_obj = models.TextField(null=True, editable=False)
    class Admin:
        list_display = ('question', ) 
    def __str__(self):
        if len(self.question) > 100:
            return self.question[0:100] + '...'
        else:
            return self.question
    def build_question_object(self, new_data):
        """ So we build the actual question object from the type template, pickle it and save the 
	    base64 encoded version of the pickled object in the database """
        qobj = eval('%s()' % QTYPES[self.question_type][1])
        qobj.save_choice_config(new_data)
        qstr = pickle.dumps(qobj, protocol=pickle.HIGHEST_PROTOCOL)
        self.question_obj = base64.b64encode(qstr)
        self.save()
    def get_question_object(self):
        qstr = base64.b64decode(self.question_obj)
        return pickle.loads(qstr)

class Survey(models.Model):
    title = models.CharField(_('Survey Title'), max_length=256)
    introduction = models.TextField(_('Survey Introduction'))
    questions = models.ManyToManyField(Question, editable=False)
    swimmers_only = models.BooleanField()
    class Admin:
        list_display = ('title', 'get_fq_url')
    def __str__(self):
        return self.title
    def get_fq_url(self):
        current_site = Site.objects.get(pk=settings.SITE_ID)
        return '<a href="http://%s/survey/%d/">http://%s/survey/%d/</a>' %(current_site.domain, self.id, current_site.domain, self.id)
    get_fq_url.allow_tags = True
    get_fq_url.short_description = 'Survey URL'
    def get_absolute_url(self):
        return '/survey/%d/' %(self.id)
    def get_ordered_questions(self):
        qps = QuestionPlace.objects.filter(survey__id__exact=self.id).order_by('place')
        if qps.count() > 0:
            return [ qp.question for qp in qps ]
        else:
            return [ q for q in self.questions.all() ]
class QuestionPlace(models.Model):
    survey = models.ForeignKey(Survey)
    question = models.ForeignKey(Question)
    place = models.IntegerField(_('Place'))
    class Meta:
        unique_together = (('survey', 'question', 'place'),)

""" If one of these exist for the survey then a swimmer has filled out the survey """
class SwimmerToSurvey(models.Model):
    swimmer = models.ForeignKey(Swimmer, editable=False)
    survey = models.ForeignKey(Survey, editable=False)
    class Meta:
        verbose_name = ('Swimmer survey record')
        verbose_name_plural = ('Swimmer survey records')
    class Admin:
        list_display = ('swimmer', 'survey',)
        list_filter = ('survey',)
        search_fields = ('swimmer__user__first_name', 'swimmer__user__last_name', )

""" Answers """
class Answer(models.Model):
    survey = models.ForeignKey(Survey, editable=False)
    question = models.ForeignKey(Question, editable=False)
    answer = models.TextField()
    class Admin:
        list_display = ('question', 'answer', )
        list_filter = ('survey', )
    def __str__(self):
        return self.answer
