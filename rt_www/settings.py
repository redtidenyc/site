# Django settings for rt_www project.
from os.path import abspath, dirname, join
DEBUG = True
TEMPLATE_DEBUG = False
DEVELOPMENT = True
PROJECT_DIR = abspath(join(dirname(__file__), '..'))

ADMINS = ( 'Anna Armentrout', 'atrout@pipeline.com' ),

MANAGERS = ADMINS

EMAIL_HOST="127.0.0.1"
DEFAULT_FROM_EMAIL="no-reply@redtidenyc.org"
SERVER_EMAIL='webmaster@redtidenyc.org'
BUSINESS_EMAIL = ''
GWORKOUTMAPKEY = 'ABQIAAAAYqa6s-bNkRjmADkuRu7JbBQxLqNj2hAR5Oqh9rxhcVklPUuKdhQx0Ct8xcE_mRKFNVS-dtxppBxHqA'
ACCOUNT='redtide-paypal-test'

isDevServer = True

if isDevServer:
    thePath = PROJECT_DIR
    OUTGOING_MAIL_HOST = '127.0.0.1'
    GWORKOUTMAPKEY = 'ABQIAAAAYqa6s-bNkRjmADkuRu7JbBQxLqNj2hAR5Oqh9rxhcVklPUuKdhQx0Ct8xcE_mRKFNVS-dtxppBxHqA'
else:
    thePath = '/home/redtide-mods'
    OUTGOING_MAIL_HOST = '127.0.0.1'
    GWORKOUTMAPKEY = 'ABQIAAAAYqa6s-bNkRjmADkuRu7JbBQxLqNj2hAR5Oqh9rxhcVklPUuKdhQx0Ct8xcE_mRKFNVS-dtxppBxHqA'
    ACCOUNT='redtide-paypal'

DATABASE_ENGINE = 'sqlite3' # 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = '%s/rt.db' % thePath            # Or path to database file if using sqlite3.
ROOT = '%s/rt_www' % thePath
SVNREPOS = '/home/svn/redtide'

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'America/New_York EST5EDT SystemV/EST5EDT US/Eastern'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'
SVNREPOS = '/home/svn/redtide'
SITE_ID = 1

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '%s/rt_www/media/' % thePath
BACKUPDIR = '%s/backups' % MEDIA_ROOT


# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '3s&li2khi0ae8)spgzrm4gk!cpr(9-r&=yu4@o%4)jj$!f5-)&'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.core.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'rt_www.flatpages.middleware.FlatpageFallbackMiddleware',
    #'rt_www.payments.middleware.PaymentsMiddleware',
    'rt_www.jsonrpclib.middleware.JSONRPCMiddleware',
)

ROOT_URLCONF = 'rt_www.urls'

TEMPLATE_DIRS = (
    '%s/rt_www/templates' % thePath,
)

AUTHENTICATION_BACKENDS = ('rt_www.swimmers.models.RTAuthBackend',)

#AUTH_PROFILE_MODULE = ( 'rt_www.swimmers.models.Swimmer', )

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.markup',
    #'rt_www.auth',
    # 'survey',
    # 'photologue',
    'rt_www.index',
    'rt_www.swimmers',
    #'rt_www.registration',
    #'rt_www.admin',
    'rt_www.mailinglist',
    'rt_www.photogallery',
    'rt_www.backups',
    #'rt_www.payments',
    'rt_www.sitemaps',
    'rt_www.flatpages',
    'rt_www.old_survey',
)
