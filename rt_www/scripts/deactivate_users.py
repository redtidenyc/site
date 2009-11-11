#!/usr/bin/env python

"""
    This goes through and sets all the users who do not have a valid annual membership in the
current period to inactive. I think this really only needs to be run like once a year. On the first
of january.
"""
import sys
from optparse import OptionParser
import datetime

from django.contrib.auth.models import User

from rt_www.registration.views import get_annual_plan
from rt_www.registration.models import Registration, Payment, PAID, Plan
from rt_www.swimmers.models import Swimmer

def get_current_coaches_plan():

    return Plan.objects.get(name__icontains='%d Coach' % datetime.datetime.now().year)

def main():
    usage = 'usage: %prog [ options ] arg'
    parser = OptionParser()
    parser.add_option('-f', '--fakeit', dest='fakeit', action='store_true',
        help='This causes a list of the users who would be deactivated to be printed to the terminal')
    (options, args) = parser.parse_args()
    annual_plan = get_annual_plan()
    coaches_plan = get_current_coaches_plan()
    """ Get the set of swimmers who have no corresponding registration object attached to a current annual plan thats paid """
    for s in Swimmer.objects.filter(user__is_active=True):
        try:
            r = Registration.objects.get(swimmer__id__exact=s.id, plan__id__in=[ annual_plan.id, coaches_plan.id ],
                registration_status__exact=PAID)
        except Registration.DoesNotExist:
            print >> sys.stderr, 'Deactivating %s' % s
            if not options.fakeit:
                s.user.is_active = False
                s.user.save()

if __name__ == '__main__':
    main()
