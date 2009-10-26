from django.utils.translation import gettext_lazy as _
from django.db import models
import os
# Create your models here.

BACKUP_TYPES = (
	( 0, 'Database'),
	( 1, 'Code repository'),
)

DB = 0
SVN = 1

class Backup(models.Model):
	file = models.CharField(_('Filename'), max_length=256, null=False, blank=False)
	date_taken = models.DateTimeField(_('Date of Backup'), auto_now_add=True)
	type = models.IntegerField(_('Type of Backup'), choices=BACKUP_TYPES)
	class Meta:
		ordering = ( '-date_taken', )
	
	def delete(self):
		try:
			os.unlink(self.file)
		except OSError:
			pass
		super(Backup, self).delete()
