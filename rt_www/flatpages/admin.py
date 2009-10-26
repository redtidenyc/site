from django.contrib import admin 
from rt_www.flatpages.models import FlatPage

class FlatPageAdmin(admin.ModelAdmin):
        fields = (
            (None, {'fields': ('url', 'title', 'content', 'sites')}),
            ('Advanced options', {'classes': 'collapse', 'fields': ('enable_comments', 'registration_required', 'template_name', 'mimetype')}),
        )
        list_filter = ('sites',)
        js = ( 'js/MochiKit/MochiKit.js', 'js/fckeditor/fckeditor.js', 'js/admin/textareas.js', )
        search_fields = ('url', 'title')

