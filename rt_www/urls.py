from django.conf.urls.defaults import *
from django.http import Http404
from rt_www.sitemaps import GenericSitemap, FlatPageSitemap
from rt_www.index.models import Blog, BlogSitemap, IndexSitemap, Announcement, Meet
from rt_www.swimmers.models import Coach
from rt_www.survey.models import Survey
from rt_www.index.views import get_current_season, get_current_year
from datetime import datetime, date
from django.contrib import admin
	
admin.autodiscover()

about_info_dict = {
    'queryset':Coach.objects.filter(is_active__exact=True).order_by('-title'), 
    'template_name':'index/about.html'
}

meets_info_dict = {
    'queryset':Meet.objects.filter(date_start__gte=datetime.now(), entry_link__isnull=False, 
        date_start__year=get_current_year()).order_by('date_start')[:5],
    'template_name':'index/meets.html',
    'extra_context':{ 'results':Meet.objects.filter(date_start__lte=datetime.now(), 
        results_link__isnull=False).exclude(results_link__exact='').order_by('-date_start')[:5], 'year':get_current_year() }
}

blogs_info_dict = { 
        'queryset':Blog.objects.all(),
        'template_name':'index/blog.html'
}

blog_info_dict = { 
    'queryset':Blog.objects.all(),
    'template_name':'index/blog.html'
}


survey_info_dict = {
    'queryset':Survey.objects.all(),
    'template_name':'survey/index.html'
}

sitemaps = {
    'index':IndexSitemap, 
    'about':GenericSitemap({'set_date':date(datetime.now().year, datetime.now().month, 1)  }, 
        priority=0.7, changefreq='monthly', location='/about/'),
    'fltapages':FlatPageSitemap,
    'meets':GenericSitemap({'set_date':date(datetime.now().year, datetime.now().month, 1)  }, 
        priority=0.7, changefreq='weekly', location='/meets/'),
    'blogs':BlogSitemap
}



urlpatterns = patterns('',
    (r'^$', 'rt_www.index.views.index'),
    (r'^sitemap.xml$', 'rt_www.sitemaps.views.sitemap', { 'sitemaps':sitemaps }),
    #(r'^login/$', 'rt_www.index.views.rt_login'),
    #(r'^logout/$', 'rt_www.index.views.rt_logout'),
    (r'^thank_you/$', 'django.views.generic.simple.direct_to_template', {'template':'index/thank_you.html'}),
    #(r'^prefs/', include('rt_www.userprefs.urls')),
    (r'^workout', 'rt_www.index.views.schedule'),
    (r'^robots.txt', 'rt_www.index.views.robots'),
    (r'^tinyspell', 'rt_www.index.views.spellchecker'),
    (r'^admin/photogallery/gallery/', include('rt_www.photogallery.adminurls')),
    (r'^survey/question/(\d+)/$', 'rt_www.survey.views.get_question'),
    #(r'^survey/(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', survey_info_dict),
    (r'^admin/survey/survey/(add|\d+)', 'rt_www.survey.views.survey_creator'),
    (r'^admin/', include('rt_www.admin.urls')),
    # (r'^admin/(*)', admin.site.root),
    # (r'^register/', include('rt_www.registration.urls')),
    (r'^galleries/', include('rt_www.photogallery.urls')),
    (r'^photos/', include('rt_www.photogallery.urls')),
    (r'^blog/xml/(?P<bid>\d+)/$', 'rt_www.index.views.xmlblog'),
    (r'^blog/(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', blog_info_dict),
    (r'^blogs/$', 'rt_www.index.views.blogs', blogs_info_dict),
    (r'^meets/$', 'django.views.generic.list_detail.object_list', meets_info_dict),
    (r'^about/$', 'django.views.generic.list_detail.object_list', about_info_dict),
    (r'^cgi-bin/', include('rt_www.registration.urls')),
    (r'^payments/(\d+)/', 'rt_www.registration.views.payments_process')
)
