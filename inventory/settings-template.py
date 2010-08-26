from os import path as os_path

# Django settings for lintory project.

##################################################
# START                                          #
# Settings that must be revised for demo to work #
##################################################

ADMINS = (
    ('Administrator', 'admin@example.org'),
)

# LDAP configuration
NAMES_ENGINE='LDAP'
LDAP_URI = 'ldap://ldap.example.org/'
LDAP_PORT = '389'
LDAP_PEOPLE = 'ou=People, dc=example, dc=org'
LDAP_GROUPS = 'ou=Group, dc=example, dc=org'
LDAP_BASE = 'dc=example, dc=org'
AUTHENTICATION_BACKENDS = (
 'inventory.backends.auth.LDAPBackend',
 )

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# All uploads of raw data will go to this directory.  This directory must
# exist, the webserver must have write access, and the done directory must
# exist within.
UPLOAD_DIR = "/tmp"

##################################################
# END                                            #
# Settings that must be revised for demo to work #
##################################################

# You may prefer to use a real database.
DATABASE_ENGINE = 'sqlite3'    # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = 'demo.db'      # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# regardless you may want to revise these anyway

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_DIR = os_path.abspath(os_path.split(__file__)[0])

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Australia/Melbourne'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-AU'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os_path.join(PROJECT_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/lintory_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
)

ROOT_URLCONF = 'inventory.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os_path.join(PROJECT_DIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'lintory',
    'south',
)

LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "/account/login/"
LOGOUT_URL = "/account/login/"
