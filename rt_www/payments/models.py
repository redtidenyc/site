from django import forms
from django.core import validators
from django.db import models
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.models import Site
from rt_www.registration.models import PayPalLogMsg, Plan, NOT_PAID, PAID, PENDING, CANCELLED, ENDED, Payment 
from rt_www.auth.models import User
from rt_www.swimmers.models import Swimmer
from datetime import date, datetime

import calendar, urllib, urllib2, re

def log(mesg):
    msg = PayPalLogMsg(msg=mesg)
    msg.save()

class Variable(models.Model):
    variable = models.CharField(_('Variable'), max_length=256, blank=False, null=False)
    value = models.CharField(_('Fixed Value'), max_length=256, blank=True, null=True)
    class Admin:
        list_display = ('variable', 'value',)
    def __str__(self):
        return self.variable + '=' + self.value
HTTP_METHODS = (
    (0, 'POST'),
    (1, 'GET'),
)

PROCESSORS = (
    (0, 'PaypalProcessor'),
)

class PaymentProcessor(models.Model):
    vendor_name = models.CharField(_('Payments Processor'), max_length=256, null=False, blank=False)
    vendor_slug = models.SlugField()
    http_method = models.IntegerField(_('HTTP Form Submission method'), choices=HTTP_METHODS, default=0)
    url = models.URLField(_('Vendor Payments Interface'), verify_exists=False, blank=False, null=False)
    validate_url = models.URLField(_('Vendor Verification URL'), verify_exists=False, blank=True, null=True)
    processor = models.IntegerField(_('Processor Object'), choices=PROCESSORS, default=0)
    class Meta:
        verbose_name = _('Vendor')
	verbose_name_plural = _('Vendors')
	
    class Admin:
        list_display = ('vendor_name', 'url',)
	prepopulated_fields = {'vendor_slug': ('vendor_name')}

    def __str__(self):
	return self.vendor_name
	
    def get_processor(self):
        return eval('%s()' % PROCESSORS[self.processor][1])
"""
	The fixed vars in the Account are vendor variables specific to that Account like
	business_email in paypal.  For a testing account we will actually create a separate testing account.
	The payments_url is used by the middleware so a payments_url *must* be defined.  It is the sole place 
	that a specific account can receive payments 
"""

class Account(models.Model):
    name = models.CharField(_('Account Holder'), max_length=256, blank=False, null=False)
    account_slug = models.SlugField()
    vendor = models.ForeignKey(PaymentProcessor)
    fixed_vars = models.ManyToManyField(Variable, null=True)
    vendor_token = models.CharField(_('Vendor Specific Auth Token'), max_length=512, blank=False, null=False)
    filter_interface = (fixed_vars) 
    class Meta:
        verbose_name = _('Account')
	verbose_name_plural = _('Accounts')
    class Admin:
        list_filter = ('vendor',)
	list_display = ('name', 'vendor',)
   	prepopulated_fields = {'account_slug':('name',)}
    def __str__(self):
        return self.name
    def get_payments_url(self):
        return "http://%s/payments/%d/" %( Site.objects.get_current().domain, self.id)

"""
	A new vendor requires a Processor.  Processor process packages and subscriptions.  Packages are one-off purchases 
	while subscriptions are a monthly stream of payments.  Vendor specific processors are pickled into the database.
"""

class VendorProcessor:
    """
        Every processor must be initialized with a plan array, account, and a user
    """
    def init(self, plan_arr, account, user):
        pass
    """
        This get a hash of URL values/variables for form submission to this particular vendor
    """
    def get_url_hash(self):
        pass
    """
        get_confirm is for the case in which a vendor has a callback to the original site which displays a confirmation page.
	returns None or the item names whose purchase is being confirmed
    """
    def get_confirm(self, new_data):
        pass
    """
        This creates a record of a transaction.  A Payment object is returned if there is some sort of transaction.  
        It's up to the calling code to check the paid status of the return object.  If no transaction, or a duplicate transaction
	None is returned
    """
    
    def create_transaction(self):
        pass

"""
	The Paypal Processor.  All processors require an account and a user

class PaypalConfirmManipulator():
    def __init__(self):
	self.fields = ( forms.TextField(field_name='tx', is_required=True), )
class PaypalProcessManipulator():
    def __init__(self):
        self.fields = (
	    forms.TextField(field_name='tx'),
            forms.TextField(field_name='custom', is_required=True),
            forms.TextField(field_name='txn_id', is_required=False), #If we get a subscr_id instead we can just ignore it
            forms.TextField(field_name='txn_type', is_required=True),
            forms.TextField(field_name='payer_email', is_required=True),
            forms.TextField(field_name='payment_status'),
            forms.IntegerField(field_name='num_cart_items'),
            forms.DecimalField(field_name='payment_gross', max_digits=10, decimal_places=2),
            forms.TextField(field_name='mc_currency', validator_list=[self.isUSD], is_required=True),
	)
    def isUSD(self, field_data, all_data):
        if not field_data == 'USD':
	    raise validators.ValidationError('Not in dollars')
"""

"""

	This is a generic payment object.  It is up to the calling code to do what it will with this
"""
class ProcessorFailure(Exception):
    pass

class ProcessUnverifiedFailed(ProcessorFailure):
    def __str__(self):
        return 'Failed on transaction verification'

class ProcessVerifiedFailed(ProcessorFailure):
    def __str__(self):
        return 'Failed on verified transaction'

class ProcessDupPayment(ProcessorFailure):
    def __init__(self, txn_id):
        self.txn_id = txn_id
    def __str__(self):
        return 'Duplicate transaction on txn_id = %s' % str(self.txn_id)

class UserNotFound(ProcessorFailure):
    def __str__(self):
        return 'Bad Swimmer ID passed from processor'	

class GenericPayment:
    plans = {}
    payment_status = NOT_PAID
    user = None
    subscr = False
    pending = False
    total_paid = 0.00
    payment_id = ''
    def add_plan(self, plan):
        self.plans[plan.id] = plan
    
    def set_user(self, user):
        self.user = user
    
    def set_payment_id(self, txn_id):
        self.payment_id = txn_id

    def get_payment_id(self):
        return self.payment_id

    def __getitem__(self, key):
        return self.plans[key]	

    def is_paid(self):
        return self.payment_status == PAID
	
    def is_cancelled(self):
        return self.payment_status == CANCELLED

    def is_ended(self):
        return self.payment_status == ENDED
    
    def set_paid(self):
        self.payment_status = PAID

    def set_cancelled(self):
        self.payment_status = CANCELLED
	
    def set_pending(self):
        self.pending = True
        
    def unset_pending(self):
        self.pending = False
    
    def is_pending(self):
        return self.pending
    
    def get_user(self):
        return self.user

    def set_subscription(self):
        self.subscr = True

    def is_subscription(self):
        return self.subscr
	
    def get_plans(self):
        return self.plans.values()


class PaypalProcessor(VendorProcessor):
    subscription_scale = 0.85
	
    def init(self, plan_arr, account, user):
        self.packages = []
        self.subscriptions = []
        for p in plan_arr:
	    if p.isrecurring:
	        self.subscriptions.append(p)
	    else:
		self.packages.append(p)
		
        self.account = account
        self.duration = 0
        self.cmd = '_cart'
        if len(self.subscriptions) > 0:
            """ Special Case:  If we have a subscription that will only last a month and part of another we treat it 
	        like a one off payment.  Remember All subscriptions stop and must be restarted at the end of each year.
	        This is a Paypal specific issue
	    """
	    self.duration = self.calc_duration()
	    if self.duration > 1:
	        self.cmd = '_xclick-subscriptions'
	
        self.user = user
	self.count = 1
	self.cart_plans = []
	self.subscrip_plans = []
	self.owed_now = sum([float(p.base_amount) for p in self.packages ])
    
    def set_account(self, account):
        self.account = account

    def __subscription_hash(self):
        for p in self.subscriptions:
            plan_amount = float(p.base_amount)
            plan_hash, delay = self.calc_delay(plan_amount)
            if self.duration <= 1:
                phash = { 'plan_name':'item_name_%d' % self.count, 'plan_name_value':'%s' %( p.name ),
                        'plan_number_name':'item_number_%d' % self.count,
                        'plan_number_value':'%d' % p.id,
                        'plan_cart_amount_name':'amount_%d' % self.count,
                        'plan_cart_amount_value':self.owed_now,
                        'plan_quantity_name':'quantity_%d' % self.count,
                        'plan_quantity_value':1  }
				
                for k, v in phash.items():
                    plan_hash[k] = v
				
                
                if self.duration == 1:
                    self.plan_set.append(plan_hash)
                    self.count += 1
                    plan_hash = { 'plan_name':'item_name_%d' % self.count, 'plan_name_value':'%s' %( p.name),
                                'plan_number_name':'item_number_%d' % self.count,
                                'plan_number_value':'%d' % p.id, 'plan_cart_amount_name':'amount_%d' % self.count,
                                'plan_cart_amount_value':plan_amount, 'plan_quantity_name':'quantity_%d' % self.count,
                                'plan_quantity_value':'1' }
			
            else:
                self.subscrip_plans.append(plan_hash)
                self.count += 1
                plan_hash = {'plan_amount_name':'a3', 'plan_amount_value':plan_amount, 'plan_period_name':'p3', 'plan_period_units_name':'t3',
                            'plan_period_value':1, 'plan_period_units_value':'M' }
				
            self.count += 1
            self.subscrip_plans.append(plan_hash)	

    def calc_duration(self):
        year, month, day = datetime.now().year, datetime.now().month, datetime.now().day
        day_discard, month_days = calendar.monthrange(year, month)
        days_left = month_days - (day - 1)
        duration = 0
        original_month = month
		
        if month == 12 and day > 5:
            month = 1
	
        duration = 12 - month
        if days_left == 0 or (original_month == 12 and month == 1):
            duration += 1
        return duration
	
    """
        This is based on the old calc_delay_duration in registration.views circa rev. 477
    """	
	
    def calc_delay(self, plan_amount):
        year, month, day = datetime.now().year, datetime.now().month, datetime.now().day
        day_discard, month_days = calendar.monthrange(year, month)
        days_left = month_days - (day - 1)
        plan_hash = {}
        duration = 0
        original_month = month
        if month < 12:
            self.owed_now += self.prorate_subscription(plan_amount)
        
        elif month == 12 and day > 5: #We are implicitly assuming that anyone registering after the 5 of december is registering for next season
            month = 1
        
        duration = 12 - month
        owed_now = '%0.2lf' % self.owed_now
        """ In the last"""
        if days_left > 0 and duration > 0:
            plan_hash['plan_amount_value'] = owed_now
            plan_hash['plan_amount_name'] = 'a1'
            plan_hash['plan_period_name'] = 'p1'
            plan_hash['plan_period_value'] = days_left
            plan_hash['plan_period_units_name'] = 't1'
            plan_hash['plan_period_units_value'] = 'D'

        if days_left == 0 or (original_month == 12 and month == 1):
            duration += 1

        return plan_hash, days_left
	
    def prorate_subscription(self, plan_amount):
        year, month, day = datetime.now().year, datetime.now().month, datetime.now().day
        day_discard, month_days = calendar.monthrange(year, month)
        day_rate = plan_amount / month_days
        """ We need to subtract 1 from the day since we don't want to prorate on the 1st of the month. """
        return plan_amount - ((day - 1) * day_rate * self.subscription_scale)

    def __package_hash(self):
        for p in self.packages:
            plan_amount = float(p.base_amount)
            self.cart_plans.append({ 'plan_name':'item_name_%d' % self.count, 'plan_name_value':p.name,
                'plan_number_name':'item_number_%d' % self.count, 'plan_number_value':'%d' % p.id,
                'plan_cart_amount_name':'amount_%d' % self.count, 'plan_cart_amount_value':plan_amount,
                'plan_quantity_name':'quantity_%d' % self.count, 'plan_quantity_value':'1' })
            self.count += 1

    def get_url_hash(self):
        payname = ' and '.join([p.description for p in self.packages + self.subscriptions ])
        try:
            custom = '%d|' % self.user.id + '|'.join([ '%d' % p.id for p in self.packages + self.subscriptions ])
        except AttributeError:
            #It used to be the case that swimmer objects utilized users as foreign keys instead of OneToOne
            custom = '%d|' % self.user.user.id + '|'.join([ '%d' % p.id for p in self.packages + self.subscriptions ])
			
        global_hash = { 'cmd':self.cmd, 'custom':custom, 'item_name':payname, 'notify_url':self.account.get_payments_url(),
	                'srt':'%d' % self.duration, 'vendor_link':self.account.vendor.url }

        self.__package_hash()
        self.__subscription_hash()
		
        for var in self.account.fixed_vars.all():
            global_hash[var.variable] = var.value
		
        for plan in self.cart_plans:
            global_hash[plan['plan_name']] = plan['plan_name_value']
            global_hash[plan['plan_number_name']] = plan['plan_number_value']
            global_hash[plan['plan_cart_amount_name']] = plan['plan_cart_amount_value']
            global_hash[plan['plan_quantity_name']] = plan['plan_quantity_value']
		
        for plan in self.subscrip_plans:
            global_hash[plan['plan_amount_name']] = plan['plan_amount_value']
            global_hash[plan['plan_period_name']] = plan['plan_period_value']
            global_hash[plan['plan_period_units_name']] = plan['plan_period_units_value']
					
        return global_hash
		
    def get_confirm(self, new_data):
        plans = [] 
        manipulator = PaypalConfirmManipulator()
        errors = manipulator.get_validation_errors(new_data)
        response_hash = {}
        if not errors:
            manipulator.do_html2python(new_data)
            transaction = new_data['tx']
            url = self.account.vendor.validate_url
            req = urllib2.Request(url, urllib.urlencode({'tx':transaction, 'cmd':'_notify-synch', 'at':self.account.vendor_token}))
            resp = None
            
            try:
                resp = urllib2.urlopen(req)
            except urllib2.URLError, e:
                log('url error like %s' % e)
                return [], {}

            firstname, lastname, total = '', '', ''
            response_values = resp.readlines()
            message = response_values[0]
            if message == 'SUCCESS\n' or message == 'VERIFIED':
                response_values.remove(message)
                for i in response_values:
                    key, value = i.split('=')
                    response_hash[key] = urllib.unquote(value.strip())
                if new_data.has_key('cm'):
                    for pid in new_data['cm'].split('|')[1:]:
                        try:
                            plan = Plan.objects.get(pk=pid)
                            plans.append(plan)
                        except KeyError:
                            break
                        except Plan.DoesNotExist:
                            continue
                elif response_hash.has_key('num_cart_items'):
                    for i in range(1, 10000):
                        try:
                            item_number = response_hash['item_number%d' %i ]
                            plan = Plan.objects.get(pk=item_number)
                            plans.append(plan)
                        except KeyError:
                            break
                        except Plan.DoesNotExist:
                            continue
            resp.close()
        return plans, response_hash

    def create_transaction(self, new_data):
        params = new_data      
        payment = GenericPayment()
        manipulator = PaypalProcessManipulator()
        errors = manipulator.get_validation_errors(new_data)
        if not errors:
            params['cmd'] = '_notify-validate'
            params = urllib.urlencode(params)
            manipulator.do_html2python(new_data)
            ppsend = self.account.vendor.validate_url
            req = urllib2.Request(ppsend, params)
            req.add_header('Content-type', 'application/x-www-form-urlencoded') 
            resp = None
            try:
                resp = urllib2.urlopen(req)
            except Exception, e:
                log('request error on %s like %s' %( ppsend, e))
                return payment
            r = resp.read()
            log('Request response was %s' % r)
            if r == 'VERIFIED':
                log('Verified transaction on the following params %s' % params)
                txn_id, custom, txn_type = None, new_data['custom'], new_data['txn_type'] 
                if new_data.has_key('txn_id'):
                    txn_id = new_data['txn_id']
                    payment.set_payment_id(txn_id)
                payment_status, payer_email = new_data['payment_status'], new_data['payer_email']
                if custom == '':
                    log('Ignoring IPN notification of non registration payment')
                    raise ProcessVerifiedFailed()
                
                try:
                    payment_obj = Payment.objects.filter(paypal_trans_id__exact=txn_id).order_by('paid_date')[0]
                    raise ProcessDupPayment(txn_id)
                except: #IndexError or something
                    pass
		
                sid, plan_hash = int(custom.split('|')[0]), {}
                pid_arr = [ int(i) for i in custom.split('|')[1:]]
                try:
                    self.user = Swimmer.objects.get(pk=sid, user__last_name__iexact=new_data['last_name'], user__first_name__iexact=new_data['first_name'])
                    payment.set_user(self.user)
                except Swimmer.DoesNotExist:
                    from django.db import connection
                    cursor = connection.cursor()
                    cursor.execute('select user_id from uid_swimmer_map where swimmer_id = %d limit 1' % sid)
                    row = cursor.fetchone()
                    try:
                        if row is not None:
                            self.user = Swimmer.objects.get(pk=row[0])
                        else: #What is happening here is that names may not match
                            self.user = Swimmer.objects.get(pk=sid)
                        payment.set_user(self.user)
		    except Swimmer.DoesNotExist:
                        raise UserNotFound()

                for pid in pid_arr:
                    try:
                        p = Plan.objects.get(pk=pid)
                        plan_hash['%d' % p.id] = p
                    except Plan.DoesNotExist:
                        continue
                
                if payment_status in ['Completed', 'Processed']:
                    payment.set_paid()
                
                elif payment_status == 'Pending':
                    payment.set_pending()
				
                payment.total_paid = new_data['payment_gross']
                if txn_type == 'cart':
                    for pid, plan in plan_hash.iteritems():
                        payment.add_plan(plan)
						
                elif re.search('subscr', txn_type):
                    payment.set_subscription()
                    if txn_type in ['subscr_cancel', 'subscr_eot']:
                        payment.set_cancelled()
                    elif ( txn_type == 'subscr_payment' ) and ( payment_status in ['Completed', 'Processed'] ):
                        payment.set_paid()
                    elif ( txn_type == 'subscr_payment' and payment_status == 'Pending' ):
                        payment.set_pending()
		
                    for pid, plan in plan_hash.iteritems():
                        payment.add_plan(plan)
        else:
            log('errors = %s' % errors)
        return payment 

class PaymentResponse(HttpResponse):
    def set_account(self, account):
        self._account = account
    def set_swimmer(self, swimmer):
        self._swimmer = swimmer
    def set_swimmer_account_plans(self, swimmer, account, plans):
        self._swimmer, self._account, self._planarr = swimmer, account, plans	
