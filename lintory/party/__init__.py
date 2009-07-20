from django.conf import settings

if not settings.NAMES_ENGINE:
    settings.NAMES_ENGINE = 'ldap'

backend = __import__('lintory.party.backends.%s'%(settings.NAMES_ENGINE), {}, {}, [''])

connection = backend.Names()
Not_Found_Error = backend.Not_Found_Error
Lookup_Error = backend.Lookup_Error
