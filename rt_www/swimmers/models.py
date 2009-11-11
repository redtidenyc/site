from django.db import models
from django import forms
#from django.core import validators
from django.utils.translation import gettext_lazy as _
from django.utils.datastructures import MultiValueDict
from django.contrib.auth.models import UserManager, User, Group, Permission
from django.conf import settings

class RTAuthBackend:
    def authenticate(self, username=None, password=None):
        user = None
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        if not user.check_password(password):
            return None
        else:
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

# US state table
class State( models.Model):
    name = models.CharField(max_length=32)
    code = models.CharField(max_length=2)
    class Meta:
        verbose_name = _('State')
        verbose_name_plural = _('States')
        ordering = ( 'id',)
    def __unicode__(self):
        return self.name

def build_state_choices():
    return tuple([ (s.id, s.code) for s in State.objects.all() ])

GENDERS = (
    ('M', 'Male'),
    ('F', 'Female'),
)

class Swimmer( models.Model):
    user = models.ForeignKey(User, unique=True)
    street = models.CharField( _('Street'), max_length=32)
    street2 = models.CharField( _('Street2'), max_length=32, blank=True)
    city = models.CharField(_('City'), max_length=32)
    state = models.ForeignKey( State )
    zipcode = models.CharField(_('Zip Code'), max_length=16 )
    usms_code = models.CharField(_('USMS Code'), max_length=10 )
    date_of_birth = models.DateField(_('Date of Birth'))
    day_phone = models.CharField(_('Day Phone'), max_length=15, blank=True, null=True)
    evening_phone = models.CharField(_('Evening Phone'), max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDERS)
    class Meta:
        verbose_name = _('Swimmer')
        verbose_name_plural = _('swimmers')

    def name(self):
        return '%s' % self.user.get_full_name()
    def email(self):
        return '%s' % self.user.email
    def age(self):
        from datetime import date
        import math
        return '%d' % math.floor((date.today() - self.date_of_birth).days/365.242199)
    def __unicode__(self):
        return '%s %s' %(self.user.first_name, self.user.last_name)

class BoardPosition( models.Model ):
    title = models.CharField(max_length=20)
    description = models.TextField()

    def __unicode__(self):
        return self.title

class BoardMember( models.Model ):
    swimmer = models.OneToOneField(User)
    position = models.ForeignKey(BoardPosition)

    def __unicode__(self):
        return '%s %s' % (self.swimmer, self.position.title)

COACH_POSITIONS = (
    ('H', 'Head Coach'),
    ('A', 'Assistant Coach'),
)
class Coach( models.Model ):
    swimmer = models.OneToOneField(User)
    title = models.CharField(_('Position Title'), max_length=1, choices=COACH_POSITIONS, default='A')
    bio = models.TextField(_('A Short Biography'), blank=False, null=False)
    is_active = models.BooleanField(default=False)
    class Meta:
        verbose_name = _( 'Coach')
        verbose_name_plural = _( 'Coaches' )

    def __unicode__(self):
        return '%s' % self.swimmer
