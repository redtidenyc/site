from django.db import models
from django.utils.translation import gettext_lazy as _
from rt_www.swimmers.models import Swimmer


# Create your models here.
class Forward(models.Model):
	swimmer = models.ForeignKey(Swimmer)
	forward = models.EmailField(unique=True)
	class Admin:
		list_display = ( 'forward', 'swimmer', )
	def __str__(self):
		return self.forward

class MailingList(models.Model):
	listaddress = models.EmailField(_('List'), unique=True)
	description = models.TextField(_('Description'), null=True, blank=True)
	ismandatory = models.BooleanField(_('Enrollment is Mandatory'))
	swimmers = models.ManyToManyField(Swimmer)
	board_postable_only = models.BooleanField(_('Only Board Members Can Post?'), default=False)
	admin_sendable_only = models.BooleanField(_('Admin Sendable?'), default=False)
	filter_interface = ('swimmers') 
	class Admin:
		list_display = ( 'listaddress', 'description', )
	def __str__(self):
		return self.listaddress

class RTMessage(models.Model):
	fromswimmer = models.ForeignKey(Swimmer)
	tolist = models.ForeignKey(MailingList)
	message = models.TextField(blank=False)
	subject = models.TextField(blank=True, null=True)
	datesent = models.DateField(_('Date Sent'), auto_now_add=True)

	class Meta:
		verbose_name = _('Message', )
		verbose_name_plural = _('Messages', )
		ordering = ( 'datesent', )
	class Admin:
		list_display = ( 'full_name', 'datesent', 'tolist', 'subject', )
		list_filter = ( 'tolist', 'datesent', )
		search_fields = ( 'message', 'fromswimmer__user__first_name', 'fromswimmer__user__last_name', 'subject', )
	def full_name(self):
		return self.fromswimmer.user.first_name + ' ' + self.fromswimmer.user.last_name
	def __str__(self):
		return self.full_name()
