from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover();

if settings.USE_I18N:
	i18n_view = 'django.views.i18n.javascript_catalog'
else:
	i18n_view = 'django.views.i18n.null_javascript_catalog'

urlpatterns = patterns('',
	('^$', 'rt_www.admin.views.main.index'),
	('^r/(\d+)/(.*)/$', 'django.views.defaults.shortcut'),
	('^jsi18n/$', i18n_view, {'packages': 'django.conf'}),
	('^logout/$', 'rt_www.auth.views.logout'),
	('^password_change/$', 'rt_www.auth.views.password_change'),
	('^password_change/done/$', 'rt_www.auth.views.password_change_done'),
	('^template_validator/$', 'rt_www.admin.views.template.template_validator'),

	# Documentation
	('^doc/$', 'rt_www.admin.views.doc.doc_index'),
	('^doc/bookmarklets/$', 'rt_www.admin.views.doc.bookmarklets'),
	('^doc/tags/$', 'rt_www.admin.views.doc.template_tag_index'),
	('^doc/filters/$', 'rt_www.admin.views.doc.template_filter_index'),
	('^doc/views/$', 'rt_www.admin.views.doc.view_index'),
	('^doc/views/jump/$', 'rt_www.admin.views.doc.jump_to_view'),
	('^doc/views/(?P<view>[^/]+)/$', 'rt_www.admin.views.doc.view_detail'),
	('^doc/models/$', 'rt_www.admin.views.doc.model_index'),
	('^doc/models/(?P<app_label>[^\.]+)\.(?P<model_name>[^/]+)/$', 'rt_www.admin.views.doc.model_detail'),
#	('^doc/templates/$', 'django.views.admin.doc.template_index'),
	('^doc/templates/(?P<template>.*)/$', 'rt_www.admin.views.doc.template_detail'),

	# Add/change/delete/history
	('^([^/]+)/([^/]+)/$', 'rt_www.admin.views.main.change_list'),
	('^([^/]+)/([^/]+)/add/$', 'rt_www.admin.views.main.add_stage'),
	('^([^/]+)/([^/]+)/(.+)/history/$', 'rt_www.admin.views.main.history'),
	('^([^/]+)/([^/]+)/(.+)/delete/$', 'rt_www.admin.views.main.delete_stage'),
	('^([^/]+)/([^/]+)/(.+)/$', 'rt_www.admin.views.main.change_stage'),
)

del i18n_view
