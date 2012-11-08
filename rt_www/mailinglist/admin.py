from django.contrib import admin
from rt_www.mailinglist.models import MailingList, RTMessage, Forward
from rt_www.swimmers.models import Swimmer

from django.utils.translation import gettext_lazy as _

class MailingListAdmin(admin.ModelAdmin):
	list_display = ( 'listaddress', 'description', )

admin.site.register(MailingList, MailingListAdmin)

class ForwardAdmin( admin.ModelAdmin ):
    list_display = ( 'forward', 'swimmer', )

	class Media:
        js = ('js/MochiKit/MochiKit.js', 'js/autocomplete.js', 'js/admin/SwimmerAutoCompleter.js',)

admin.site.register(Forward, ForwardAdmin)

class RTMessageAdmin(admin.ModelAdmin):
	list_display = ( 'full_name', 'datesent', 'tolist', 'subject', )
	list_filter = ( 'tolist', 'datesent', )
	search_fields = ( 'message', 'fromswimmer__user__first_name', 'fromswimmer__user__last_name', 'subject', )

admin.site.register(RTMessage, RTMessageAdmin)