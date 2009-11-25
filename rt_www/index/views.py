import urllib, re, random, xml.dom.minidom #, aspell
from datetime import datetime

from django.conf import settings
from django.template import Context, loader, RequestContext, TemplateDoesNotExist
from django.shortcuts import render_to_response
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django import forms
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list

from rt_www.index.models import Meet, Blog, Announcement, Closing, Schedule, Practice, DAYS
from rt_www.swimmers.models import Coach

def blogs(*args, **kwargs):
    try:
        kwargs['extra_context'] = { 'object':Blog.objects.latest('pub_date') }
    except:
        pass
    return object_list(*args, **kwargs)

def xmlblog(request, bid):
    try:
        b = Blog.objects.get(pk=bid)
        t = loader.get_template('index/blog.xml')
        return HttpResponse(t.render(Context({'text':b.text})), mimetype='application/xml')
    except Blog.DoesNotExist:
        return HttpResponseNotFound()

""" For now this just spits a stock robots.txt back at the user later we add some smarts in here for custom client programs"""
def robots(request):
    response = HttpResponse(mimetype='text/plain')
    response.write('User-agent: *\nAllow: /\nDisallow: /admin\nDisallow: /cgi-bin')
    return response

def get_current_season():
    season = ''
    current_schedule = None
    try:
        current_schedule = Schedule.objects.filter(date_start__lte=datetime.now(),
            date_end__gte=datetime.now()).latest('date_end')
    except Schedule.DoesNotExist:
        pass

    if current_schedule != None:
        year_interval = current_schedule.date_start.strftime('%Y')
        if current_schedule.date_start.year != current_schedule.date_end.year:
            year_interval = '%s - %s' %( current_schedule.date_start.strftime('%Y'),
                current_schedule.date_end.strftime('%Y') )

        return '%s %s' %( current_schedule.season, year_interval )

def get_current_year():
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    if month == 12 and day > 15:
        year = year + 1

    return '%s' %( year )

def index(request):
    announcements = Announcement.objects.filter(expiration_date__gte=datetime.now())
    current_announcements = []
    for an in announcements:
        current_announcements.append({'fptext':an.fptext, 'title':an.title })
    current_closings = Closing.objects.filter(close_date_start__gte=datetime.now())
    current_schedule = None
    season = ''
    practices = []
    try:
        current_schedule = Schedule.objects.filter(date_start__lte=datetime.now(), date_end__gte=datetime.now()).latest('date_end')
    except:
        pass
    if current_schedule != None:
        practices = [ {'day':DAYS[p.day][1], 'period':p.start_time.strftime('%p'),
                'start':p.start_time.strftime('%I:%M'),
                'end':p.end_time.strftime('%I:%M'),
                'pool':p.pool.name } for p in current_schedule.practices.all().order_by('day', 'start_time') ]
        season = '%s - %s' %( current_schedule.date_start.strftime('%m/%d/%y'),
                        current_schedule.date_end.strftime('%m/%d/%y') )

    return render_to_response('index/index.html',
        { 'current_announcements':current_announcements,
          'current_closings':current_closings,
                  'season':season,
          'practices':practices }, context_instance=RequestContext(request))

def schedule(request):
    current_schedule = None
    season = ''
    practices = []
    try:
        current_schedule = Schedule.objects.filter(date_start__lte=datetime.now(), date_end__gte=datetime.now()).latest('date_end')
    except Schedule.DoesNotExist:
        pass
    if current_schedule != None:
        practices = [ {'day':DAYS[p.day][1], 'period':p.start_time.strftime('%p'),
                'start':p.start_time.strftime('%I:%M'),
                'end':p.end_time.strftime('%I:%M'), 'pool':p.pool.name }
                                for p in current_schedule.practices.all().order_by('day', 'start_time') ]

        season = '%s - %s' %( current_schedule.date_start.strftime('%B %d, %Y'),
                        current_schedule.date_end.strftime('%B %d, %Y') )
    return render_to_response('index/workout.html', { 'google_key':settings.GWORKOUTMAPKEY, 'season':season,
        'practices':practices }, context_instance=RequestContext(request))

def rt_login(request):
    errors = []
    if request.POST:
        username, password = request.POST['username'], request.POST['password']
        next = ''
        if request.POST.has_key('next'):
            next = request.POST['next']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if next == '':
                    return HttpResponseRedirect('/prefs/%d/' % user.id)
                else:
                    return HttpResponseRedirect(next)
            else:
                errors = ['Account is disabled']
        else:
            errors = ['Invalid Login']
    else:
        errors = ['Invalid Login']
    return render_to_response('index/login.html', {'errors':errors}, context_instance=RequestContext(request))

def rt_logout(request):
    logout(request)
    return HttpResponseRedirect('/thank_you/')
"""
class RegisterLoginForm(forms.Manipulator):
    def __init__(self):
        self.fields = (
            forms.EmailField(field_name='email', validators=[ self.isValidUser, self.isPasswordSet ], is_required=True)
        )

    def isValidUser(self, field_data, all_data):
        try:
            user = User.objects.get(email__iexact=field_data)
        except User.DoesNotExist:
            raise validators.ValidationError('Invalid email.  Either the user attached to this email is inactive or does not exist')
    def isPasswordSet(self, field_data, all_data):
        try:
            user = user.objects.get(email__iexact=field_data, password__exact='')
        except User.DoesNotExist:
            raise validators.ValidationError('Invalid email.  Either the user attached to this email is inactive or does not exist')
"""


def register_login(request):
    errors = new_data = {}
    manipulator = RegisterLoginForm()
    if request.POST or request.GET:
        if request.POST:
            new_data = request.POST.copy()
        elif request.GET:
            new_data = request.GET.copy()
        errors = manipulator.get_validation_errors(new_data)
        manipulator.do_html2python(new_data)
        if not errors:
            user = User.objects.get(email__iexact-new_data['email'])
            random_pass = ''.join([ random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQURSTUVWXYZ0123456789')
                    for i in range(15) ])
            user.set_password(random_pass)
            t = loader.get_template('index/set_password_email.txt')
            c = Context({ 'password':random_pass, 'first_name':user.first_name })
            message = t.render(c)
            send_mail('Welcome to Your Redtide Area', message, 'webmaster@redtidenyc.org',
                [ user.email ], fail_silently=True)

def forums(request):
        return render_to_response('index/forums.html', {}, context_instance=RequestContext(request))

""" We are using aspell-python for spell checking """
"""
class URLDecodeTextField(forms.TextField):
    def convert_post_data(self, new_data):
        name = self.get_member_name()
        converted_data = []
        if new_data.has_key(self.field_name):
            dlist = new_data.getlist(self.field_name)
            converted_data = [ urllib.unquote_plus(d) for d in dlist ]
        new_data.setlist(name, converted_data)

class BooleanTextField(forms.TextField):
    def convert_post_data(self, new_data):
        name = self.get_member_name()
        converted_data = []
        if new_data.has_key(self.field_name):
            dlist = new_data.getlist(self.field_name)
            converted_data = [ d == 'true' for d in dlist ]
        new_data.setlist(name, converted_data)
"""

"""
class SpellcheckerManipulator(forms.Manipulator):
    def __init__(self):
        self.fields = (
            forms.TextField(field_name='id', is_required=True),
            URLDecodeTextField(field_name='check', is_required=True),
            forms.TextField(field_name='cmd', is_required=True),
            forms.TextField(field_name='lang'),
            forms.TextField(field_name='mode'),
            forms.TextField(field_name='spelling'),
            forms.TextField(field_name='jargon'),
            forms.TextField(field_name='encoding'),
            BooleanTextField(field_name='sg'),
        )
"""

def spellchecker(request):
    jargon, lang, mode, spelling = '', 'en', '', ''
    new_data = errors = {}
    #manipulator = SpellcheckerManipulator()
    impl = xml.dom.minidom.getDOMImplementation()
    doc = impl.createDocument(None, None, None)
    if request.POST or request.GET:
        if request.POST:
            new_data = request.POST.copy()
        else:
            new_data = request.GET.copy()
        errors = manipulator.get_validation_errors(new_data)
        manipulator.do_html2python(new_data)
        root = doc.createElement('res')
        root.setAttribute('id', new_data['id'])
        root.setAttribute('cmd', new_data['cmd'])
        if not errors:
            speller = aspell.Speller(('lang', 'en'))
            if new_data['cmd'] == 'spell':
                words = re.split('\s+', new_data['check'])
                results = [ word for word in words if speller.check(word) == 0 ]
            elif new_data['cmd'] == 'suggest':
                results = speller.suggest(new_data['check'])
            if len(results) > 0:
                rchild = doc.createTextNode(urllib.quote_plus(' '.join(results)))
                root.appendChild(rchild)
        else:
            root.setAttribute('error', 'true')
            root.setAttribute('msg', ' '.join(errors.items()))
        doc.appendChild(root)
    return HttpResponse(doc.toxml(), mimetype='application/xml')
