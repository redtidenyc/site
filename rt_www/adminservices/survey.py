from rt_www.survey.models import Survey, Question, Answer, QTYPES

"""
	Load all the Question Types
"""

qtypes = [ qtype[1] for qtype in QTYPES ]
mod = __import__('rt_www.survey.models', globals(), locals(), qtypes)
for qt in qtypes:
	globals()['%s' % qt] = getattr(mod, qt)

class Service:
	def delete_question(self, qid):
		try:
			q = Question.objects.get(pk=int(qid))
			q.delete()
		except Question.DoesNotExist, e:
			raise e
		return qid
	
	def get_type_mapping(self):
		ret_val = {}
		for qt in QTYPES:
			ret_val[str(qt[0])] = qt[1]
		return ret_val
	
	def get_type_options(self, opt):
		question_type = None
		for qt in QTYPES:
			if qt[0] == int(opt):
				question_type = eval('%s()' % qt[1])
				break
		if question_type != None:
			return question_type.create_choice_widget()
		else:
			raise Exception('Invalid Question Type')
	def save_question(self, question, qtype, data_hash):
		q = Question(question=question, question_type=int(qtype))
		q.save()
		q.build_question_object(data_hash)
		question = '%s' % q
		return { 'question':question, 'qid':q.id }
	def edit_question(self, question, qid, data_hash):
		try:
			q = Question.objects.get(pk=int(qid))
			q.question = question
			q.save()
                        q.build_question_object(data_hash)
			q.save()
		except Question.DoesNotExist, e:
			raise e
		return { 'question':question, 'qid':qid }
	def get_question(self, qid):
		try:
			q = Question.objects.get(pk=int(qid))
		except Question.DoesNotExist, e:
			raise e 
		qobj = q.get_question_object()
		ret_val = qobj.get_edit_hash()
		ret_val['question'] = q.question
		ret_val['qid'] = q.id
		return ret_val
	
service = Service()			
