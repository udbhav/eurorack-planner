import os

# Abspath discovery
def p(*args):
    return os.path.realpath(os.path.join(*args))

DEBUG = False
TEMPLATE_DEBUG = True  # By default for Sentry

ADMINS = (
    ("Udbhav Gupta", "gupta.udbhav@gmail.com"),
)

MANAGERS = ADMINS

# Set this in your source/settings/local.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',
    }
}

TIME_ZONE = "America/New_York"
LANGUAGE_CODE = "en-us"

SITE_ID = 1

# Internationalization machinery
USE_I18N = False
# Date Format
USE_L10N = False

# This dynamically discovers the path to the project
PROJECT_PATH = p(os.path.dirname(__file__), '../')
MEDIA_ROOT = p(PROJECT_PATH, '../media')
MEDIA_URL = '/media/'
STATIC_ROOT = p(PROJECT_PATH, "../statique/")
STATIC_URL = '/static/'
LOG_ROOT = p(PROJECT_PATH, '../../logs/')

STATICFILES_DIRS = (
    p(PROJECT_PATH, '../static/'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

ADMIN_MEDIA_PREFIX = '%sadmin/' % STATIC_URL

# Set this in your local_settings.py
SECRET_KEY = ''

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
    # Cache is always first!
    'django.middleware.cache.UpdateCacheMiddleware',

    # Django middleware
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    # Third party middleware
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',

    # Cache fetch is always last!
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'urls'

# Find the template dirs automatically
TEMPLATE_DIRS = (p(PROJECT_PATH, 'templates'),)

# Project Apps: Keep these seperate for testing
PROJECT_APPS = (
    'apps.modules',
    'apps.search',
)

INSTALLED_APPS = (
    # Django Applications
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Third Party Django Applications
    'haystack',
    'debug_toolbar',
    'django_extensions',
    'gunicorn',
    'south',
    'compressor',
    'storages',
    'registration',
    'django_forms_bootstrap',
    'imagekit',
    'djcelery',

) + PROJECT_APPS

TEMPLATE_TAGS = (
)

# Set in source/settings/local.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.',
    }
}

# Haystack
HAYSTACK_SITECONF = 'search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = p(PROJECT_PATH, '../whoosh_index')

# Django Compressor
COMPRESS_PRECOMPILERS = (
     ('text/less', 'lessc {infile} {outfile}'), 
)

# Debug Toolbar
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'HIDE_DJANGO_SQL': True,
}
INTERNAL_IPS = ("127.0.0.1",)


# Django Registration
ACCOUNT_ACTIVATION_DAYS = 14
LOGIN_REDIRECT_URL = '/'

# Email
DEFAULT_FROM_EMAIL = 'noreply@eurorackplanner.com'

# Celery
import djcelery
djcelery.setup_loader()
BROKER_URL = 'redis://'
