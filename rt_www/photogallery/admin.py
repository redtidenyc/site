from django.contrib import admin

from photogallery.models import Video, Photo, Gallery, PhotoPlace

class VideoAdmin(admin.ModelAdmin):
    list_display = ('thumb_link', 'title', 'date_uploaded',)
    list_filter = ('date_uploaded',)

admin.site.register(Video, VideoAdmin)

class PhotoAdmin(admin.ModelAdmin):
    list_display = ( 'thumb', 'title', 'photographer', 'gallery',)
    list_filter = ( 'gallery', )
    list_display_links = ( 'thumb', )
    js = ('js/MochiKit/MochiKit.js', 'js/autocomplete.js', 'js/admin/PhotoManager.js',)
admin.site.register(Photo, PhotoAdmin)

class GalleryAdmin(admin.ModelAdmin):
    ordering = ['date']
    list_display = ( 'title', 'creator')
admin.site.register(Gallery, GalleryAdmin)

class PhotoPlaceAdmin(admin.ModelAdmin):
    pass
admin.site.register(PhotoPlace, PhotoPlaceAdmin)