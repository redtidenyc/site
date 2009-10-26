from django.db.models import Q
from rt_www.swimmers.models import Swimmer
from rt_www.auth.models import User

class Service:
    def get_swimmers(self, match):
        slist = []
	#This is ugly but there is an open bug in django that causes this
	swimmers = Swimmer.objects.select_related().order_by('auth_user.first_name').filter( 
		    Q(user__first_name__icontains = match) | Q(user__last_name__icontains = match))
	return [ {'value':'%s %s' %( s.user.first_name, s.user.last_name ), 'id':s.user.id }  for s in swimmers if s.user.is_active ]
 
    def get_users(self, match):
        users = User.objects.filter(Q(first_name__icontains = match) | Q(last_name__icontains = match)).order_by('first_name') 
        return [ {'value':'%s %s' %( u.first_name, u.last_name ), 'id':u.id } for u in users if u.is_active  ]

service = Service()
