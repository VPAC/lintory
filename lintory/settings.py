SITE_ID = 1
SESSION_COOKIE_SECURE = True

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
STATIC_ROOT = "/usr/share/lintory/static"

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
STATIC_URL = '/lintory/media/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.static",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
)

ROOT_URLCONF = 'lintory.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "/etc/lintory/templates",
)

INSTALLED_APPS = (
    'django_webs',
    'lintory',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'south',
    'ajax_select',
    'django_tables2',
)

LOGIN_URL = "/lintory/account/login/"
LOGIN_REDIRECT_URL = "/lintory"
LOGOUT_URL = "/lintory/account/login/"

AJAX_LOOKUP_CHANNELS = {
    'party' : ('lintory.lookup', 'party_lookup'),
    'location' : ('lintory.lookup', 'location_lookup'),
    'software' : ('lintory.lookup', 'software_lookup'),
}
AJAX_SELECT_BOOTSTRAP = False
AJAX_SELECT_INLINES = None

DEFAULT_CONTENT_TYPE = "application/xhtml+xml"

execfile("/etc/lintory/settings.py")
