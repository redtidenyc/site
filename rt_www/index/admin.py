from django.contrib import admin
from rt_www.index.models import Announcement, Blog, Pool, Practice, Schedule, Closing, Meet

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'expiration_date', )
    list_filter = ( 'pub_date', 'expiration_date', )

    class Media:
        js = ( 'js/MochiKit/MochiKit.js', 'js/fckeditor/fckeditor.js', 'js/admin/textareas.js', )

admin.site.register(Announcement, AnnouncementAdmin)

class BlogAdmin(admin.ModelAdmin):
    list_display = ('author', 'blurb', 'pub_date', 'get_fq_url', )
    list_filter = ('pub_date', )

    class Media:
        js = ( 'js/fckeditor/fckeditor.js','js/MochiKit/MochiKit.js', 'js/autocomplete.js', 'js/admin/Blog.js',  )

admin.site.register(Blog, BlogAdmin)

class PoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', )

admin.site.register(Pool, PoolAdmin)

class PracticeAdmin(admin.ModelAdmin):
    list_display = ( 'pool', 'start_time', 'end_time', 'day' )

admin.site.register(Practice, PracticeAdmin)


class ScheduleAdmin(admin.ModelAdmin):
        list_display = ('season', 'date_start', 'date_end' )

admin.site.register(Schedule, ScheduleAdmin)

class ClosingAdmin(admin.ModelAdmin):
       list_display = ('pool', 'close_date_start', 'close_date_end', )

admin.site.register(Closing, ClosingAdmin)

class MeetAdmin(admin.ModelAdmin):
        list_display = ('name', 'date_start', 'date_end')
        list_filter = ('us_state', 'date_start',)

admin.site.register(Meet, MeetAdmin)
