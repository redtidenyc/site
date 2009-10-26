from rt_www.swimmers.models import State, Swimmer
from rt_www.registration.models import Plan, Registration, NOT_PAID, PAID, PENDING, CANCELLED, ENDED 
from rt_www.registration.views import get_annual_plan
from datetime import datetime, date
import re


class Service:
    def getstates(self):
        return [ { 'code':s.code, 'id':s.id } for s in State.objects.all() ]
    
    def getplans(self):
        plans = Plan.objects.filter(reg_period__period_start__lte=datetime.now(), reg_period__period_end__gte=datetime.now())
        planhash = []
        for p in plans:
            name = ' '.join([ n.capitalize() for n in (p.name).split(' ') ])
            planhash.append({'name':name + ' - $ %0.2lf' % p.base_amount, 'id':p.id})
        return planhash

    def lookup(self, email, dob):
        userhash = {'error':[]}
        try:
	    dob = date(int(dob[4:8]), int(dob[0:2]), int(dob[2:4]))
	except ValueError: #Catches invalid dates
	    userhash['error'] = ['Invalid date. Check that the date of birth and email are correct.']
	    return userhash
				
	try:
	    swimmer = Swimmer.objects.get(user__email__iexact=email, date_of_birth__exact=dob)
	except Swimmer.DoesNotExist:
	    userhash['error'] = ['Swimmer is not in the database. Check that the date of birth and email are correct.']
            return userhash

	usms = ''
	usms_reg = re.compile('^\w{2}(\d{1})')
	m = usms_reg.search(swimmer.usms_code)
	if m:
	    usms_year = m.group(1)
	    current_year = str(datetime.now().year)[-1]
	    next_year = str(datetime.now().year + 1)[-1]
	    if usms_year == next_year  and datetime.now().month == 12 and datetime.now().day >= 1:
	        usms = swimmer.usms_code
	    elif usms_year == current_year and datetime.now().month < 12:
	        usms = swimmer.usms_code
				
            swimmer_dict = { 'firstname':swimmer.user.first_name, 'lastname':swimmer.user.last_name, \
			    'email':swimmer.user.email, 'address':swimmer.street, 'address2':swimmer.street2, \
			    'usms':usms, 'city':swimmer.city, 'state':swimmer.state.id, 'zip':swimmer.zipcode, \
			    'dob':swimmer.date_of_birth.strftime('%m%d%Y'), 'dayphone':swimmer.day_phone, 
			    'evephone':swimmer.evening_phone, 'gender':swimmer.gender,
			    'sid':swimmer.user.id }
	    for k, v in swimmer_dict.items():
	        userhash[k] = v

	return userhash

    def calcowed(self, plan, sid):
	ret_val = { 'plans':[], 'owed':0.0 }
	plan_ids = []
	owed = 0.0
	annual_plan = get_annual_plan()
	pid, sid, swimmer, double, owed = int(plan), int(sid), None, True, 0
	annual_paid = False
	plan_paid = False
	if sid > 0:
	    """ First check if they've already paid for the annual membership
	    """		
	    r = Registration.objects.filter(swimmer__exact=sid,
		    plan__id__exact=annual_plan.id,
		    registration_status__in=[PAID,PENDING],
		    plan__reg_period__period_start__lte=datetime.now(),
		    plan__reg_period__period_end__gte=datetime.now())
	    if len(r) > 0:
	        annual_paid = True

	        """ If we were only trying to register annual, return now.
		"""
		if pid == annual_plan.id:
		    plan_ids.append(pid)
		    owed = 0.0
		    ret_val['owed'] = '%0.2lf' % owed
		    ret_val['plans'] = plan_ids
		    return ret_val

	    """ If they are trying to buy a recurring package they've 
	        already paid for we deal with that
	    """
	    r = Registration.objects.filter(swimmer__exact=sid, 
	            plan__id__exact=pid,
		    registration_status__exact=PAID,
		    plan__isrecurring__exact=True,
		    plan__reg_period__period_start__lte=datetime.now(), 
		    plan__reg_period__period_end__gte=datetime.now())
	    if len(r) > 0:
	        plan_paid = True	

	        """
	        If we've already paid for annual return now
		"""
		if annual_paid:
		    owed += 0.0
		    plan_ids.append(pid) 
		    ret_val['plans'] = plan_ids
		    ret_val['owed'] = '%0.2lf' % owed 
		    return ret_val
	
        """
            After this point we are looking at a new swimmer
        """
        pidPlan = Plan.objects.get(pk=pid)
	if not plan_paid: 
	    owed += pidPlan.base_amount
			
	if pidPlan.add_annual and ( not annual_paid ):
	    plan_ids.append(annual_plan.id)
	    owed += int(annual_plan.base_amount)

	
        plan_ids.append(pid)	
        ret_val['plans'] = plan_ids
	ret_val['owed'] = '%0.2lf' % owed	
	ret_val['annual'] = annual_plan.id

	return ret_val

service = Service()
