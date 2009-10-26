#!/usr/bin/python

import sys, os, re

from rt_www.registration.models import Registration, Plan, PAID
from rt_www.mailinglist.models import MailingList, Message
from rt_www.swimmers.models import Swimmer
from rt_www.registration.views import get_annual_plan
from optparse import OptionParser


def main():

	usage = 'usage: %prog [options] arg'
	parser = OptionParser()
	parser.add_option('-p', '--package', dest='package', help='The name or package id used as condition of enrollment')
	parser.add_option('-l', '--list', dest='list', help='The list email address to enroll everyone in')
	parser.add_option('-c', '--clearlist', action='store_true', dest='clear', help='Clear out the mailing list.')
	parser.add_option('-i', '--inactive', action='store_true', dest='inactive', help='Only add inactive users')
	(options, args) = parser.parse_args()
	if not options.list:
		parser.error('a list need to be defined')
	
	try:
		mlist = MailingList.objects.get(listaddress__exact=options.list)
	except MailingList.ListDoesNotExist:
		parser.error('invalid list passed through')
	
	if options.clear:
		print >> sys.stderr, 'Clearing list %s' % options.list
		mlist.swimmers.clear()
		mlist.save()
		return

	plan = None
	if options.package:
		if re.match('^\d+$', options.package):
			package_id = int(options.package)
			try:
				plan = Plan.objects.get(pk=package_id)
			except Plan.DoesNotExist:
				parser.error('plan id %d does not exist' % package_id )
		else:
			package_name = options.package
			try:
				plan = Plan.objects.get(name__icontains=package_name)
			except plans.PlanDoesNotExist:
				parser.error('plan id %d does not exist' % package_id )
			
	else:
		 plan = get_annual_plan()
	if not plan:
		print >>sys.stderr, 'There is something really wrong, can\'t find any valid plans'
		os.exit(1)
	registrants = []
	if not options.inactive:
		registrants = Registration.objects.filter(plan__id__exact=plan.id, registration_status__exact=PAID)
	else:
		registrants = Registration.objects.filter(swimmer__user__is_active=False, plan__id__exact=plan.id, registration_status__exact=PAID)
		
	mlist.swimmers = [ r.swimmer for r in registrants ]
	mlist.save()
	return

if __name__ == '__main__':
	main()
