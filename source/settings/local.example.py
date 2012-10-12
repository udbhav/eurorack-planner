from settings.default import *

SITE_ID = 1
DEBUG = True
LOCAL_SERVE = True
SOUTH_TESTS_MIGRATE = False

# Dummy cache for development
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Set session engine to db so that our session doesn't get lost without cache
SESSION_ENGINE = "django.contrib.sessions.backends.db"

# DB
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'eurorack-planner.sqlite'
    }
}

# Debug Toolbar
SHOW_DEBUG_TOOLBAR = True
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'HIDE_DJANGO_SQL': True,
 }

# Email testing
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
