from django.db import models
from django.contrib.localflavor.us.models import PhoneNumberField
from django.conf import settings
from django.core import validators
from rt_www.sitemaps import Sitemap, ping_google
from rt_www.swimmers.models import State, Swimmer
from rt_www.siteutils import strip_html
from django.contrib.sites.models import Site
from datetime import datetime

class Announcement(models.Model):
    fptext = models.TextField('Short blurb for the front page')
    title = models.CharField(max_length=200)
    pub_date = models.DateField('Date Published', default=datetime.now)
    expiration_date = models.DateField('Date to Expire', default=datetime.now)
    class Meta:
	ordering = [ '-pub_date' ]
    class Admin:
	js = ( 'js/MochiKit/MochiKit.js', 'js/fckeditor/fckeditor.js', 'js/admin/textareas.js', )
	list_display = ('title', 'pub_date', 'expiration_date', )
	list_filter = ( 'pub_date', 'expiration_date', )
	
    def __str__(self):
        return self.title
    def get_absolute_url(self):
	return '/announcements/'
    def get_text(self):
	return self.fptext
	
    def save(self):
	super(Announcement, self).save()
	try:
	    ping_google()
	except Exception:
	    pass

class Blog(models.Model):
    title = models.CharField(max_length=256, blank=False)
    text = models.TextField('Blog Entry', blank=False, null=False)
    pub_date = models.DateTimeField('Date Published', default=datetime.now)
    author = models.ForeignKey(Swimmer)
    class Meta:
	ordering = [ '-pub_date' ]

    class Admin:
        js = ( 'js/fckeditor/fckeditor.js','js/MochiKit/MochiKit.js', 'js/autocomplete.js', 'js/admin/Blog.js',  )
        list_display = ('author', 'blurb', 'pub_date', 'get_fq_url', )
        list_filter = ('pub_date', )
    
    def get_fq_url(self):
        current_site = Site.objects.get(pk=settings.SITE_ID)
        return '<a href="http://%s/blog/%d/">http://%s/blog/%d/</a>' %(current_site.domain, self.id, current_site.domain, self.id)
    get_fq_url.allow_tags = True
    get_fq_url.short_description = 'Blog URL'
    
    def blurb(self):
        return '%s' % str(self)
    def short_name(self):
        return '%s. %s' %( self.author.user.first_name[0].upper(), self.author.user.last_name.capitalize())
    def __str__(self):
        if len(self.text) > 100:
            return strip_html(self.text[0:100])
        else:
            return strip_html(self.text)

class IndexSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9
    location = '/'
    def items(self):
        return [ Announcement.objects.all().latest('pub_date') ]
    def lastmod(self, obj):
        return obj.pub_date

class BlogSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.8
    location = '/blogs/'
    def items(self):
        try:
            return [ Blog.objects.all().latest('pub_date') ]
        except Blog.DoesNotExist:
            return []
    def lastmod(self, obj):
        try:
            return obj.pub_date
        except:
            return ''

class Pool(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    zip = models.CharField(max_length=5)
    email_address = models.EmailField(blank=True)
    phone1 = PhoneNumberField(blank=True)
    contact_name = models.CharField(max_length=100, blank=True)
    directions = models.TextField()
    short_name = models.CharField(max_length=3, null=True, blank=True)

    def __str__(self):
        return self.name
	
    class Admin:
	list_display = ('name', 'address', )

DAYS = (
    ( 0, 'Sunday' ),
    ( 1, 'Monday' ),
    ( 2, 'Tuesday' ),
    ( 3, 'Wednesday' ),
    ( 4, 'Thursday' ),
    ( 5, 'Friday' ),
    ( 6, 'Saturday' ),
)

class Practice(models.Model):
    pool = models.ForeignKey(Pool)
    start_time = models.TimeField('Practice Start')
    end_time = models.TimeField('Practice End')
    day = models.IntegerField('Week Day', choices=DAYS)
    def __str__(self):
        DAYS = ( 
	    ( 0, 'Sunday' ), 
	    ( 1, 'Monday' ), 
	    ( 2, 'Tuesday' ), 
	    ( 3, 'Wednesday' ), 
	    ( 4, 'Thursday' ), 
	    ( 5, 'Friday' ), 
	    ( 6, 'Saturday' ), 
	)	
	return '%s\t%s-%s' %( DAYS[int(self.day)][1], self.start_time, self.end_time )	
    class Meta:
	ordering = [ 'day' ]
	
    class Admin:
	list_display = ( 'pool', 'start_time', 'end_time', 'day' )
		

class Schedule(models.Model):
    practices = models.ManyToManyField(Practice)
    season = models.CharField('Season', max_length=50)
    date_start = models.DateField('Season Start')
    date_end = models.DateField('Season End')
    filter_horizontal = ('practice')

    class Admin:
        list_display = ('season', 'date_start', 'date_end' )
		
class Closing(models.Model):
    pool = models.ForeignKey(Pool)
    close_date_start = models.DateField('Closing Date Start')
    close_date_end = models.DateField('Closing Date End', blank=True, null=True)
    reason = models.CharField(max_length=200, blank=True)

    class Admin:
        list_display = ('pool', 'close_date_start', 'close_date_end', )
		
    def __str__(self):
	ret_val = self.close_date_start.strftime('%m/%d')
	if self.close_date_end != None:
	    ret_val += '-' + self.close_date_end.strftime('%m/%d')
	ret_val += ' ' + self.pool.short_name
	return ret_val

class Meet(models.Model):
    name = models.CharField(max_length=100)
    date_start = models.DateField('Meet Start')
    date_end = models.DateField('Meet End', blank=True, null=True)
    date_close = models.DateField('Meet Registration Closes', blank=True, null=True)
    entry_link = models.URLField(verify_exists=True)
    results_link = models.URLField(verify_exists=False, blank=True, null=True)
    meet_pool = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.ForeignKey(State, blank=True, null=True)
    country = models.CharField('Country', max_length=200, default="United States", blank=True, null=False)
	
    class Meta:
        ordering = ('-date_start',)
	
    class Admin:
        list_display = ('name', 'date_start', 'date_end')
        list_filter = ('state', 'date_start',)
    def __str__(self):
	return self.name

    def get_display_date(self):
        ret_val = '%s' % self.date_start.strftime('%B %d')
        if self.date_end:
            ret_val += '-%s' % self.date_end.strftime('%d')
        return ret_val
