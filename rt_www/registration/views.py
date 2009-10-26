from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response
from rt_www.index.models import Schedule
from rt_www.index.views import get_current_season
from rt_www.swimmers.models import Swimmer, State, GENDERS
from rt_www.auth.models import User
from rt_www.registration.models import Payment, PayPalLogMsg, Period, Plan, Registration, NOT_PAID, PAID, PENDING, CANCELLED, ENDED
from rt_www.mailinglist.models import MailingList
from rt_www.payments.models import Account, GenericPayment, PaymentResponse, log
from django.conf import settings
from datetime import datetime, date
from django.http import HttpResponse
from django.conf import settings 
from django import forms
from django.core import validators
import re, math, string, simplejson, urllib2, urllib, calendar

def mailinglist_subscribe(swimmer):
    mailinglists = MailingList.objects.filter(ismandatory__exact=True)
    for mailinglist in mailinglists:
        try:
            swimmer.mailinglist_set.get(pk=mailinglist.id)
        except MailingList.DoesNotExist:
            swimmer.mailinglist_set.add(mailinglist)
    swimmer.save()

def get_annual_plan():
    current_year = datetime.now().year
    period_start = date(year=current_year, month=1, day=1)
    period_end = date(year=current_year, month=12, day=31)
		
    if datetime.now().month == 12 and datetime.now().day >= 5:
        period_start = date(year=current_year,month=11,day=1) 
	current_year += 1
	"""period_start = date(year=current_year, month=1, day=1)
	"""
	period_end = date(year=current_year, month=12, day=31)
			
    try:
	current_period = Period.objects.get(period_start__exact=period_start, period_end__exact=period_end)
    except Period.DoesNotExist:
        log('period doesnt exist')
	current_period = Period(period_start=period_start, period_end=period_end)
	current_period.save()
			
    try:
	annual_plan = Plan.objects.get(name__exact='%d Annual Membership' % current_year)
    except Plan.DoesNotExist:
	log('plan doesnt exist')
	annual_plan = Plan(name='%d Annual Membership' % current_year, base_amount=40.00, reg_period=current_period)
	annual_plan.save()
    return annual_plan	

""" 
	This form is really used for validation more then anything
"""

class PlanField(forms.IntegerField):
    def convert_post_data(self, new_data):
        name = self.get_member_name()
	if new_data.has_key(self.field_name):
	    d = new_data.getlist(self.field_name)
	    try:
		converted_data = [ Plan.objects.get(pk=d[0]) ]
	    except Plan.DoesNotExist:
		converted_data = []
	    except IndexError:
		converted_data = []
	    new_data.setlist(name, converted_data)
	else:
	    new_data.setlist(name, [])

class StateField(forms.SelectField):
    def convert_post_data(self, new_data):
        name = self.get_member_name()
	if new_data.has_key(self.field_name):
	    d = new_data.getlist(self.field_name)
	    try:
	        converted_data = [ State.objects.get(pk=d[0]) ]
	    except Plan.DoesNotExist:
		converted_data = []
	    except IndexError:
		converted_data = []
	    new_data.setlist(name, converted_data)
	else:
	    new_data.setlist(name, [])
	
class RegistrationManipulator(forms.Manipulator):
    def __init__(self):
        states = tuple([ (s.id, s.code) for s in State.objects.all() ]) 
	self.fields = (
	    forms.PasswordField(field_name='password', is_required=False),
	    forms.TextField(field_name='firstname', max_length=100, is_required=True),
	    forms.TextField(field_name='middle', max_length=1),
	    forms.TextField(field_name='lastname', max_length=100, is_required=True),
	    forms.EmailField(field_name='email', is_required=True),
	    forms.TextField(field_name='usms', length=10, max_length=10, is_required=True),
	    forms.TextField(field_name='address', max_length=256, is_required=True),
	    forms.TextField(field_name='address2', max_length=256, is_required=False),
	    forms.TextField(field_name='city', max_length=256, is_required=True),
	    StateField(field_name='state', choices=states, is_required=True),
	    forms.TextField(field_name='zip', validator_list=[ validators.isOnlyDigits ], is_required=True),
	    forms.TextField(field_name='gender', length=1, max_length=1, is_required=True),
	    forms.DateField(field_name='dob', is_required=True),
	    forms.TextField(field_name='dayphone', length=10, max_length=12, is_required=False),
	    forms.TextField(field_name='evephone', length=10, max_length=12, is_required=False),
	    forms.IntegerField(field_name='iscoach', is_required=False),
	    forms.IntegerField(field_name='terms', is_required=False),
	    PlanField(field_name='plan0', is_required=True),
	    PlanField(field_name='plan1', is_required=False),
	)
    
    def __init_swimmer(self, swimmer, new_data):
        swimmer.street, swimmer.street2 = new_data['address'], new_data['address2']
	swimmer.city, swimmer.state, swimmer.zipcode = new_data['city'], new_data['state'], new_data['zip']
	swimmer.usms_code, swimmer.date_of_birth = new_data['usms'], new_data['dob']
	swimmer.day_phone, swimmer.evening_phone = new_data['dayphone'], new_data['evephone']
	swimmer.gender = new_data['gender']
	return swimmer

    def save(self, new_data):
        new_data['firstname'] = string.capwords(new_data['firstname'])
	new_data['lastname'] = string.capwords(new_data['lastname'])
	new_data['city'] = string.capwords(new_data['city'])
	new_data['address'] = string.capwords(new_data['address'])
	new_data['address2'] = string.capwords(new_data['address2'])
	hassid = False
	swimmer = None
	if new_data.has_key('sid'):
	    try:
		swimmer = Swimmer.objects.get(pk=new_data['sid'])
		hassid = True
	    except Swimmer.DoesNotExist:
	        pass
	
        if not hassid:
	    try:
	        user = User.objects.get(email__exact=new_data['email'])
		user.first_name, user.middle_initial = new_data['firstname'], new_data['middle']
	        user.last_name = new_data['lastname']
		user.is_active = True
	    except User.DoesNotExist:
		user = User(username=new_data['email'], email=new_data['email'], password=new_data['password'],
			    is_staff=False, is_superuser=False, is_active=True, 
			    first_name=new_data['firstname'], last_name=new_data['lastname'])
	    user.save()
	    try:
	        swimmer = Swimmer.objects.get(pk=user.id)
		swimmer = self.__init_swimmer(swimmer, new_data)
	    except Swimmer.DoesNotExist:
		swimmer = Swimmer(user=user, street=new_data['address'], street2=new_data['address2'],
			city=new_data['city'], state=new_data['state'], zipcode=new_data['zip'],
			usms_code=new_data['usms'], date_of_birth=new_data['dob'],
			day_phone=new_data['dayphone'], evening_phone=new_data['evephone'], gender=new_data['gender'])
	else:
	    user = swimmer.user
	    user.first_name = new_data['firstname'], user.last_name = new_data['lastname']
	    user.email = new_data['email']
	    
            if new_data['password'] != '':
	        user.password = new_data['password']
	    user.save()
	    swimmer = self.__init_swimmer(swimmer, new_data)
	
        swimmer.save()
	return swimmer 
 

def complete(request):
    new_data = errors = {}
    manipulator = RegistrationManipulator()
    if request.GET:
        new_data = request.GET.copy()
	errors = manipulator.get_validation_errors(new_data)
        manipulator.do_html2python(new_data)
	if not errors:
	    owed = new_data['owed']
	    plan_list = [ new_data['plan%d' %i ] for i in range(2) if new_data['plan%d' %i ] ]
	    swimmer = manipulator.save(new_data)
	    user = swimmer.user
	    """ At this point we check to see if the plan sent is priced at 0 if it is then we save 
	    the registration and send them to the confirm page
	    """
	    if len(plan_list) == 1 and int(plan_list[0].base_amount) == 0:
		plan = plan_list[0]
		try:
		    r = Registration.objects.get(swimmer__exact=swimmer, plan__id__exact=plan.id,
			plan__reg_period__period_start__lte=datetime.now() ,
			plan__reg_period__period_end__gte=datetime.now())
		except Registration.DoesNotExist:
		    r = Registration(registration_date=datetime.now(), swimmer=swimmer, plan=plan)

		r.registration_status = PAID
		r.save()
			
		try:				
		    p = Payment.objects.get(swimmer__exact=swimmer, plan__id__exact=plan.id, registration__id__exact=r.id)
	        except Payment.DoesNotExist:
		    p = Payment(paypal_trans_id='nopaypal', amount_paid=0.00, swimmer=swimmer, paid_date=datetime.now(), plan_id=plan.id, registration_id=r.id )	
		p.save()
			
		""" And finally we sign people up into any mandatory mailing lists """
                """ But don't sign them out of existing ones they are in """
	        mailinglist_subscribe(swimmer)	

		return render_to_response('registration/confirm.html',{'payment_gross':'0.00', 'payment_date':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
			    'payer_email':user.email, 'first_name':user.first_name, 'last_name':user.last_name, 'mc_gross':'0.00', 'payment_type':plan.name
			}, context_instance=RequestContext(request))
	
	    annual_plan = get_annual_plan()
		
	    for plan in plan_list:
	        """ If the user already has a registration for this plan in this period
		the rules for when to create a new one are complicated
		1) Only one annual registration should exist per swimmer per year
	        2) Never create a new unlimited registration. If the old one is CANCELLED or ENDED, set it to NOT_PAID
		3) Create a new swimpass registration if the old one has been PAID
	        """
		r = Registration.objects.filter(swimmer__exact=swimmer, plan__id__exact=plan.id,
		        plan__reg_period__period_start__lte=datetime.now() ,
			plan__reg_period__period_end__gte=datetime.now())

		if len(r) > 0:
		    if plan.id == annual_plan.id:
			for reg in r:
			    reg.registration_date = datetime.now()
			    reg.save()
		    elif plan.isrecurring:
		        found = False
			for reg in r:
			    if reg.registration_status == CANCELLED or reg.registration_status == ENDED:
			        reg.registration_status = NOT_PAID
			    found = True
			    reg.registration_date = datetime.now()
			    reg.save()
			if not found:
			    reg = Registration(registration_date = datetime.now(), swimmer=swimmer, plan=plan, registration_status=NOT_PAID)
			    reg.save()
		    else:
			found = False
			for reg in r:
			    if reg.registration_status == NOT_PAID:
			        found = True
			        reg.registration_date = datetime.now()
				reg.save()
			if not found:
			    reg = Registration(registration_date = datetime.now(),swimmer = swimmer, plan=plan, registration_status=NOT_PAID)
			    reg.save() 
		else:
		    reg = Registration(registration_date=datetime.now(), swimmer=swimmer, plan=plan, registration_status=NOT_PAID)
		    reg.save()
		
                if plan.id == annual_plan.id:
		    contains_annual = True		
	    account = Account.objects.get(account_slug__exact=settings.ACCOUNT)

	    resp = PaymentResponse()
	    resp._swimmer, resp._account, resp._planarr = swimmer, account, plan_list 
	    return resp
    return HttpResponse(simplejson.dumps({'errors':[ str(e) for e in errors ]}), mimetype='application/javascript')


""" This is to handle what comes from paypal """
"""
	This is a little tricky.  When the paypal request comes in we are supposed to repost it back to paypal
	to validate.  If it vaidates we simply return a 200 OK otherwise we return nothing
"""

def test_paypal(request):
    if request.POST:
        log(request.raw_post_data)   
    return HttpResponse('VERIFIED')

def confirm(request):
    """ secure request to the PayPal server to fetch the transaction info
    """
    new_data = {}	
    if request.POST:
	new_data = request.POST.copy()
    else:
        new_data = request.GET.copy()
    
    transaction,message,instructions = '', '', ''
    month,day = datetime.now().month, datetime.now().day
    """ if it's not next year's renewal time and there is no transaction id
	    something went wrong
    """
    
    account = Account.objects.get(account_slug__exact=settings.ACCOUNT)
    processor = account.vendor.get_processor()
    processor.set_account(account)
    plans, response_hash = processor.get_confirm(new_data)
    annual_plan = get_annual_plan()
    has_annual = len([p for p in plans if p.id == annual_plan.id]) > 0
    has_monthly = len([p for p in plans if re.search('Monthly', p.name) ]) > 0
    """Annual instructions are default"""
    instructions="annual"  
    if len([ p for p in plans if re.search('Pass', p.name)]) > 0: 
        instructions="pass"
    elif has_monthly: 
	message = "Your subscription has been created."
	instructions="monthly"
    response_hash['message'] = message
    response_hash[instructions] = "true" 
    return render_to_response('registration/confirm.html', 
        response_hash, context_instance=RequestContext(request))

""" Process PayPal Payments for Redtide registration account only.  The catch here is that under the old system we told paypal 
that the notify_url = http://www.redtidenyc.org/cgi-bin/payments.cgi.  So we keep this around to answer those and only those requests

"""
def process(request):
    log('raw post_data is ' + request.raw_post_data)
    new_data = {}
    account = Account.objects.get(account_slug__exact=settings.ACCOUNT)
    processor = account.vendor.get_processor()
    processor.set_account(account)
    if request.GET or request.POST:
		
        if request.POST:
	    new_data = request.POST.copy()
	else:
	    new_data = request.GET.copy()
		
	generic_payment = processor.create_transaction(new_data)
	swimmer, txn_id = generic_payment.get_user(), generic_payment.get_payment_id()
        log('swimmer is : %s' % swimmer)
        payment_amt = generic_payment.total_paid
	annual_plan = get_annual_plan()
	if not generic_payment.is_subscription():
	    payment_amt = generic_payment.total_paid
	    plans = generic_payment.get_plans()
	    for plan in generic_payment.get_plans():
		amt_paid = float(plan.base_amount)
		leftover = float(payment_amt) - amt_paid
	        if int(math.ceil(leftover)) < 0:
		    amt_paid = float(payment_amt)
		elif int(math.floor(leftover)) > 0:
		    payment_amt = leftover
					
		r = Registration.objects.filter(plan__id__exact=plan.id, 
		    swimmer__exact=swimmer, 
		    plan__reg_period__period_start__lte=datetime.now(),
		    plan__reg_period__period_end__gte=datetime.now()).exclude(
		    registration_status__exact=PAID)
	        if len(r) <= 0:
		    log('registration not found for pid = %s and swimmerid =%s' %(plan.id, str(swimmer)))
		    continue
	        
                if len(r) > 1:
		    log('multiple registrations found for pid = %s using the first returned' % plan.id)
		r = r[0]
		stat = generic_payment.is_paid()		
		if generic_payment.is_paid():
		    r.registration_status = PAID
		    annual_plan = get_annual_plan()
		    if plan.id == annual_plan.id:
		        mailinglist_subscribe(swimmer)
		elif generic_payment.is_pending():
		    r.registration_status = PENDING
		else: #There was at least a penny unpaid
		    r.registration_status = NOT_PAID
		
                r.save()
		payment = Payment( paypal_trans_id=txn_id, amount_paid=amt_paid, swimmer=swimmer, paid_date=datetime.now(), plan_id=plan.id, registration_id=r.id)
		payment.save()
	else:
	    """ 
		  deal with failures or cancellations
	    """
	    if not generic_payment.is_paid():
		""" mark each item cancelled EXCEPT for annual if it is paid """
		for plan in generic_payment.get_plans():
		    try:
		        r = Registration.objects.get(plan__id__exact=plan.id, swimmer__exact=swimmer,
			    plan__reg_period__period_start__lte=datetime.now(),
			    plan__reg_period__period_end__gte=datetime.now())
		    except Registration.DoesNotExist:
		        log('registration not found for pid = %s and swimmerid =%d' %(plan.id, swimmer.user.id))
			continue
		    """ Annual Memberships can't be cancelled if they are already paid
		        If they are pending and the status is FAILED then mark it not paid """
		    if plan.id == annual_plan.id:
		        if r.registration_status != PAID:
			    if not generic_payment.is_cancelled():
				r.registration_status = NOT_PAID
		    else:
			if generic_payment.is_cancelled():
			    r.registration_status = CANCELLED
		        else:
			    r.registration_status = NOT_PAID
						
		    r.save()

	        """  
		now let's handle PAYMENTS 
		"""
	    else:
		""" deal with annual first, if it exists """
				
		subscr_annual = None
	        plan_arr = generic_payment.get_plans()
		plans = [ p for p in plan_arr if p.id != annual_plan.id ]
		for p in plan_arr:
		    if p.id == annual_plan.id:
			subscr_annual = p
			break
		if subscr_annual:
		    try:
		        r = Registration.objects.get(plan__id__exact=annual_plan.id, swimmer__exact=swimmer,
			        plan__reg_period__period_start__lte=datetime.now(),
				plan__reg_period__period_end__gte=datetime.now())
			""" annual plan payments can't be cancelled 
			or reset once they've been paid
			so check if this one is paid before we change the registration status
			"""
		        if r.registration_status != PAID:
	
			    amt_paid =  float(annual_plan.base_amount)
			    leftover = payment_amt - amt_paid
			    if int(math.ceil(leftover)) <= 0:
				amt_paid = float(payment_amt)
			        payment_amt = 0.0
			    elif int(math.floor(leftover)) > 0:
				payment_amt = leftover
			    
                            if generic_payment.is_pending():
				r.registration_status = PENDING
			    elif generic_payment.is_paid():
			        r.registration_status = PAID
			    r.save()

			    """ save payment """
			    payment = Payment( paypal_trans_id=txn_id, amount_paid=amt_paid, swimmer=swimmer, paid_date=datetime.now(), plan_id=annual_plan.id,
				    registration_id = r.id)
			    payment.save()
			
                        """ if they've paid, add them to the mailing lists """
		        if r.registration_status == PAID:
                            mailinglist_subscribe(swimmer)

		    except Registration.DoesNotExist:
		        log('registration not found for pid = %s and swimmerid =%d'  %(annual_plan.id, swimmer.user.id))
		""" take care of other items in the subscription """
	        for plan in plans:
		    try:
		        r = Registration.objects.get(plan__id__exact=plan.id, swimmer__exact=swimmer, plan__reg_period__period_start__lte=datetime.now(),
			    plan__reg_period__period_end__gte=datetime.now())
		    except Registration.DoesNotExist:
			log('registration not found for pid = %s and swimmerid =%d' %(plan.id, swimmer.user.id))
			continue

		    amt_paid =  float(plan.base_amount)
		    """ This payment might be less than the plan amount if it has been prorated. Record the payment if the amount is over zero. """
		    if payment_amt > 0.0:
		        leftover = payment_amt - amt_paid
		        log('leftover: %s payment_amt: %s amt_paid: %s' % (leftover, payment_amt, amt_paid))
			if int(math.ceil(leftover)) <= 0:
			    amt_paid = float(payment_amt)
			    payment_amt = 0.0
		        elif int(math.floor(leftover)) > 0:
			    payment_amt = leftover
                    if generic_payment.is_pending():
			r.registration_status = PENDING
                    elif generic_payment.is_paid():
			r.registration_status = PAID
                    r.save()
                    
                    payment = Payment( paypal_trans_id=generic_payment.get_payment_id(), amount_paid=amt_paid,
			    swimmer=swimmer, paid_date=datetime.now(),
			    plan_id=plan.id, registration_id = r.id )
		    payment.save()

	    return HttpResponse('Completed')	

    else: #Error
        log('Received weird request from %s'  % request.META['REMOTE_HOST'])
    return HttpResponse('failed to process')

"""
	This is broken but we allow for the new style urls to continue registration
"""

def payments_process(request, aid):
	account = None
        log('Received paypal call' + request.raw_post_data)
	try:
		account = Account.objects.get(pk=aid)
	except Account.DoesNotExist, e:
		raise e
	if account.account_slug == settings.ACCOUNT:
		return process(request)
	else:
		return HttpResponse()
