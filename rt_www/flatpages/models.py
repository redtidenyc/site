# from django.core import validators
from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm

class FlatPage(models.Model):
    url = models.CharField(_('URL'), max_length=100, 
        help_text=_("Example: '/about/contact/'. Make sure to have leading and trailing slashes."))
    title = models.CharField(_('title'), max_length=200)
    content = models.TextField(_('content'))
    enable_comments = models.BooleanField(_('enable comments'))
    template_name = models.CharField(_('template name'), max_length=70, blank=True,
        help_text=_("Example: 'flatpages/contact_page.html'. If this isn't provided, the system will use 'flatpages/default.html'."))
    registration_required = models.BooleanField(_('registration required'), help_text=_("If this is checked, only logged-in users will be able to view the page."))
    sites = models.ManyToManyField(Site)
    mimetype = models.CharField(_('Mimetype'), max_length=256, default='text/html')
    class Meta:
        db_table = 'django_flatpage'
        verbose_name = _('flat page')
        verbose_name_plural = _('flat pages')
        ordering = ('url',)

    def __str__(self):
        return "%s -- %s" % (self.url, self.title)

    def value_to_string(self):
        return "%s -- %s" % (self.url, self.title)

    def get_absolute_url(self):
        return self.url

    def get_model(self):
    	return FlatPageForm(self)

class FlatPageForm(ModelForm):
	class Meta:
		model = FlatPage

