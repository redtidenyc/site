from rt_www.survey.models import Question, Survey, QTYPES, Answer, SwimmerToSurvey
from rt_www.swimmers.models import Swimmer

class Service:
    def swimmer_login(self, usms):
        try:
            s = Swimmer.objects.get(usms_code__iexact=usms)
        except Swimmer.DoesNotExist:
            return -1
        if not s.user.is_active:
            return -1
        return s.user.id
    def get_question(self, qid):
        q = Question.objects.get(pk=qid)
        qobj = q.get_question_object()
        return {'id':q.id, 'type':qobj.create_choice_widget()['type'], 'data':qobj.render(), 'question':q.question }

    def get_questions(self, sid):
        """
        This get the entire set of questions and feeds it back to the client in a hash
        """
        try:
            survey = Survey.objects.get(pk=sid)
        except Survey.DoesNotExist, e:
            raise e
        questions = survey.get_ordered_questions()
        return { 'introduction':survey.introduction,
                 'data':[ { 'id':q.id, 'type':q.get_question_object().create_choice_widget()['type'],
                     'question':q.question, 'data':q.get_question_object().render() } for q in questions ] }

    def save_answers(self, answers, survey_id, uid = -1):
        uid = int(uid)
        try:
            survey = Survey.objects.get(pk=survey_id)
        except Survey.DoesNotExist, e:
            raise e

        qids = [ q.id for q in survey.questions.all() ]
        not_answered = []

        for qid in qids:
            if answers.has_key(str(qid)):
                """ The answers coming in are an array """
                for a in answers[str(qid)]:
                    ans = Answer(survey=survey, question=Question.objects.get(pk=qid), answer=a)
                    ans.save()
            else:
                not_answered.append(qid)

        if len(not_answered) == 0 and uid > 0:
            try:
                ss = SwimmerToSurvey(swimmer=Swimmer.objects.get(pk=uid), survey=survey)
                ss.save()
            except Swimmer.DoesNotExist, e:
                raise e

        return not_answered

service = Service()
