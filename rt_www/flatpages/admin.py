from django.contrib import admin

from rt_www.flatpages.models import FlatPage

class FlatPageAdmin(admin.ModelAdmin):

        list_filter = ('sites',)
        search_fields = ('url', 'title')

        class Media:
            js = ( 'js/MochiKit/MochiKit.js', 'js/fckeditor/fckeditor.js', 'js/admin/textareas.js', )

admin.site.register(FlatPage, FlatPageAdmin)