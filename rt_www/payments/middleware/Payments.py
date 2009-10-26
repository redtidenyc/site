from django.conf import settings
from django.http import HttpResponse
from rt_www.swimmers.models import Swimmer
from rt_www.payments.models import PaymentResponse
import simplejson


class PaymentsMiddleware:
	"""
		process_response - this takes the outgoing response to paypal and transforms it
		to a 302
		the outgoing response has a array of plans, and a swimmer object attached
		to it
	"""
	def process_response(self, request, response):
		if isinstance(response, PaymentResponse):
			account, processor, swimmer = response._account, response._account.vendor.get_processor(), response._swimmer	
			plans = response._planarr
			processor.init(plans, account, swimmer)
			return HttpResponse(simplejson.dumps(processor.get_url_hash()), mimetype='application/javascript')
		else:
			return response	
