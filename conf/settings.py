# Django settings for photos project.

#DEBUG = True
#TEMPLATE_DEBUG = DEBUG

ADMINS = (
#    ('Name', 'email@example.org'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '/var/lib/lintory/lintory.db', # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# LDAP configuration
LDAP_URI = 'ldap://ldap.example.org/'
LDAP_PORT = '389'
LDAP_PEOPLE = 'ou=People, dc=example, dc=org'
LDAP_GROUPS = 'ou=Group, dc=example, dc=org'
LDAP_BASE = 'dc=example, dc=org'
AUTHENTICATION_BACKENDS = (
 'inventory.backends.auth.LDAPBackend',
)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Australia/Victoria'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-AU'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

EMAIL_HOST="mail.example.org"
SERVER_EMAIL = "Name <email@example.org>"

# All uploads of raw data will go to this directory.  This directory must
# exist, the webserver must have write access, and the done directory must
# exist within.
UPLOAD_DIR = "/var/lib/lintory/data"
