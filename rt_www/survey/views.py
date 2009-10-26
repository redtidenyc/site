from django.shortcuts import render_to_response
from django.template import RequestContext as Context
from django.contrib.contenttypes.models import ContentType
from rt_www.admin.views.decorators import staff_member_required
from rt_www.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect, HttpResponse
from django.core import validators
from django import forms
from rt_www.survey.models import Survey, Question, Answer, QTYPES, QuestionPlace
import simplejson, re

class SurveyManipulator(forms.Manipulator):
    def __init__(self):
        questions = tuple([ (q.id, '%s' % q) for q in Question.objects.all()])
        self.fields = (
            forms.TextField(field_name='title', maxlength=256, is_required=True),
            forms.CheckboxField(field_name='swimmers_only'),
            forms.LargeTextField(field_name='introduction'),
	)
    def save(self, new_data):
        if new_data.has_key('survey'):
            survey = new_data['survey']
	else:
	    survey = Survey()
        survey.title = new_data['title']
        survey.swimmers_only = new_data['swimmers_only']
	if new_data['introduction'] != '':
	    survey.introduction = new_data['introduction']
	qids = [ new_data[k] for k in new_data.keys() if re.search('question\d+', k) ]
	survey.save()
	for qid in qids:
	    try:
	        question = Question.objects.get(pk=int(qid))
	    except Question.DoesNotExist, e:
	        continue
	    survey.questions.add(question)
	survey.save()
        """ Save the order now """
        key_re = re.compile('^order(\d+)$')
        for key in new_data.keys():
            m = key_re.match(key)
            if m:
                order = int(m.group(1))
                qid = int(new_data[key])
                try:
                    question = Question.objects.get(pk=qid)
                except Question.DoesNotExist:
                    continue
                try:
                    qp = QuestionPlace.objects.get(survey__id__exact=survey.id, place__exact=order)
                    qp.question = question
                except QuestionPlace.DoesNotExist:
                    try:
                        q = Question.objects.get(pk=qid)
                        qp = QuestionPlace(survey=survey, question=question, place=order)
                    except Question.DoesNotExist:
                        continue
                qp.save()
	return survey


def survey_creator(request, sid):
    new_data = errors = {}
    try:
        survey = Survey.objects.get(pk=sid)
    except Survey.DoesNotExist:
        survey = None
    if request.POST:
        #Saving a created questionnaire
        manipulator = SurveyManipulator()
        new_data = request.POST.copy()
        errors = manipulator.get_validation_errors(new_data)
        manipulator.do_html2python(new_data)
        if not errors:
            if survey is not None:
                new_data['survey'] = survey
            survey = manipulator.save(new_data)
            LogEntry.objects.log_action(request.user.id, ContentType.objects.get_for_model(Survey).id, survey.id, str(survey), CHANGE)
            msg = _('The %(name)s "%(obj)s" was successfully modified') %{ 'name':Survey._meta.verbose_name, 'obj':survey }
            if request.POST.has_key("_continue"):
                request.user.message_set.create(message=msg + ' ' + _("You may edit it again below."))
                return HttpResponseRedirect('/admin/survey/survey/%d/' % int(survey.id))
            elif request.POST.has_key("_addanother"):
                request.user.message_set.create(message=msg + ' ' + (_("You may add another %s below.") % Survey._meta.verbose_name))
                """ FIXME: I didn't have an internet connection but we need to set this path 
		to the base path of the image
		"""
                return HttpResponseRedirect('/admin/survey/survey/add/')
	    else:
	        request.user.message_set.create(message=msg)	
		return HttpResponseRedirect('/admin/survey/survey/')
	else:
	    c = Context(request, { 'errors':errors })
            return render_to_response('survey/admin/survey_form.html', {}, context_instance=c)
				
    else:
        if not survey:
            #We start with a blank form
            c = Context(request, { 'errors':errors, 'add':True, 'qtypes':QTYPES, 'survey':None })
            return render_to_response('survey/admin/survey_form.html', {}, context_instance=c)
        else:
            c = Context(request, { 'errors':errors, 'change':True, 'qtypes':QTYPES, 'survey':survey })
            return render_to_response('survey/admin/survey_form.html', {}, context_instance=c)
		
survey_creator = staff_member_required(never_cache(survey_creator))

def get_question(request, qid):
    question = None
    resp_xml = ''
    try:
        question = Question.objects.get(pk=qid)
    except Question.DoesNotExist:
        pass
    if question:
        qobj = question.get_question_object()
        resp_xml = qobj.render(question.question)
	
    return HttpResponse(resp_xml, mimetype='text/xml')
