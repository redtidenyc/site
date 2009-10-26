from django.db import models
from rt_www.index.models import Pool
from rt_www.swimmers.models import Swimmer
from django.utils.translation import gettext_lazy as _

"""
	Remember we have RTUsers and Swimmers
	I am dumping the team choice
"""

PAID_STATUS = (
	( 0, 'NOT_PAID'),
	( 1, 'PAID' ),
	( 2, 'PENDING' ),
	( 3, 'CANCELLED' ),
	( 4, 'ENDED' ),
)

NOT_PAID=0
PAID=1
PENDING=2
CANCELLED=3
ENDED=4

class PayPalLogMsg(models.Model):
	msg = models.TextField(null=False, blank=False)
	date = models.DateTimeField(auto_now_add=True)
	class Meta:
        	verbose_name = _('Paypal Log Message')
        	verbose_name_plural = _('Paypal Log Messages')
        	ordering = ('-date',)
	class Admin:
		list_display = ( 'date', 'msg', )
	
	def __str__(self):
		return self.msg
class Period(models.Model):
	period_start = models.DateField()
	period_end = models.DateField()
	class Admin:
		list_display = ( 'period_start', 'period_end', )
	def __str__(self):
		return self.period_start.strftime('%Y-%m-%d') + ' to ' + self.period_end.strftime('%Y-%m-%d')

class Plan(models.Model):
	name = models.CharField(max_length=200)
	base_amount = models.DecimalField(decimal_places=2, max_digits=6)
	late_fee = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=6)
	description = models.TextField()
	reg_period = models.ForeignKey(Period, null=True)
	swim_count = models.PositiveIntegerField(null=False, default=0, blank=True)
	add_annual = models.BooleanField(default=True)
	isrecurring = models.BooleanField(default=False)

	class Admin:
		list_display = ( 'name', 'base_amount', )

	def __str__(self):
		return self.name

class Registration(models.Model):
	"""The Registration model.  Each registration is connected to s swimmer, a date it
	happened, A specific plan and whether the registrant has paid or not, or cancelled a
	existing subscription
	"""
	
	swimmer = models.ForeignKey(Swimmer)
	registration_date = models.DateField()
	registration_status = models.IntegerField(choices=PAID_STATUS, null=True)
	plan = models.ForeignKey(Plan)
	comment = models.TextField(blank=True, null=True)

	class Admin:
		list_display = ( 'show_swimmer', 'show_plan', 'registration_date', 'show_payments',)
		list_filter = ( 'plan', 'registration_status', 'registration_date',)
		search_fields = ( 'swimmer__user__first_name', 'swimmer__user__last_name', )
	def show_plan(self):
		return '%s' % self.plan.name
	
	def __str__(self):
		return '%s - %s' %( self.swimmer, self.plan.name )

	def show_swimmer(self):
		return '%s %s' % ( self.swimmer.user.first_name, self.swimmer.user.last_name )

	def show_payments(self):
		"""
		This shows the latest payment for this particular
		registration
		"""
		payment = self.payment_set.latest('paid_date')
		if payment is not None: 
			return '%s' % payment
		else:
			return ''
	

"""
	We have several sorts of packages here.  One are things like yearly membership which is a one time payment that purchases services for a defined time
period, another is the swim pass which is a one time payment for a discrete good, and thirdly we have the monthly rebillable package.
	1. paid_status == PAID, PENDING or NOT PAID
	2. paid_status == PAID, PENDING or NOT_PAID
	3. paid_status == PAID, PENDING, NOT_PAID, CANCELLED, ENDED
	
	3. deserves some special mention.  Registration maps to multiple payments so there should exist a trail of payments through the database that
indicate the start and stop of a registration. Therefore we should probably include a plan id in the payment table, but mysteriously I decided to leave it out.
"""
	
class Payment(models.Model):
	paypal_trans_id = models.CharField(max_length=25)
	swimmer = models.ForeignKey(Swimmer)
	paid_date = models.DateField()
	amount_paid = models.DecimalField(decimal_places=2, max_digits=6)
	plan = models.ForeignKey(Plan)
	registration = models.ForeignKey(Registration)

	
	class Meta:
		ordering = ( '-paid_date', )
		
	class Admin:
		list_display = ( 'show_swimmer', 'plan', 'paypal_trans_id', 'paid_date', 'amount_paid', )
		list_filter = ( 'plan', 'paid_date', )
		search_fields = ( 'swimmer__user__first_name', 'swimmer__user__last_name', )
	
	def show_swimmer(self):
		return '%s %s' % (self.swimmer.user.first_name, self.swimmer.user.last_name )

	def __str__(self):
		ret_vars = 'Payment - ' + self.swimmer.user.get_full_name()
		ret_vars += ' for ' + self.plan.description
		ret_vars += ' paid $%s' % self.amount_paid
		ret_vars += ' %s' % self.paid_date
		return ret_vars 



