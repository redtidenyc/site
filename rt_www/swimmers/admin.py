from django.contrib import admin
from rt_www.swimmers.models import Swimmer, BoardPosition, BoardMember, Coach
from django.utils.translation import ugettext as _

class SwimmerAdmin( admin.ModelAdmin):
    fieldsets = ( (None, {'fields': ('user', )}),
            (_('Personal info'), {'fields': ('street', 'street2', 'city', 'state',
                'zipcode', 'usms_code', 'date_of_birth',
                'day_phone', 'evening_phone', 'gender')}),
        )
    list_display = ( 'name', 'age', 'usms_code', 'email', )
    list_filter = ( 'gender', 'city', 'state', )
    search_fields = ('user__first_name', 'user__last_name', 'city', )

    class Media:
        js = ('js/MochiKit/MochiKit.js', 'js/autocomplete.js', 'js/admin/UserAutoCompleter.js',)

admin.site.register(Swimmer, SwimmerAdmin)

class BoardPositionAdmin( admin.ModelAdmin ):
    list_display = ( 'title', 'description' )

admin.site.register(BoardPosition, BoardPositionAdmin)

class BoardMemberAdmin( admin.ModelAdmin ):
    list_display = ('swimmer','position',)

    class Media:
        js = ('js/MochiKit/MochiKit.js', 'js/autocomplete.js', 'js/admin/SwimmerAutoCompleter.js',)

admin.site.register(BoardMember, BoardMemberAdmin)

class CoachAdmin( admin.ModelAdmin ):
    list_display = ('swimmer','title', 'is_active')
    list_filter = ( 'is_active', 'title' )

    class Media:
        js = ('js/MochiKit/MochiKit.js', 'js/autocomplete.js', 'js/admin/SwimmerAutoCompleter.js',)

admin.site.register(Coach, CoachAdmin)
