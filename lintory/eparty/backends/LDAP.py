import ldap
import ldap.filter
from lintory.eparty.backends import *
from django.conf import settings

class Names(Names_Base):
        l = None

        def open(self):
            if self.l is not None:
                return

            try:
                self.l = ldap.initialize(settings.LDAP_URI)
            except ldap.LDAPError:
                raise Lookup_Error("Cannot connect to LDAP server.")


        def lookup_user_input(self,value):
            self.open()

            attrs = [ "cn" ]

            try:
                if value.find("=") != -1:
                    r = self.l.search_st(value, ldap.SCOPE_BASE, filterstr='(objectClass=*)', attrlist=attrs, attrsonly=0, timeout=5)
                else:
                    filter = ldap.filter.filter_format("(cn=%s)",[value])
                    r = self.l.search_st(settings.LDAP_BASE, ldap.SCOPE_SUBTREE, filter, attrlist=attrs, attrsonly=0, timeout=5)
                    if len(r)==0:
                        filter = ldap.filter.filter_format("(givenName=%s)",[value])
                        r = self.l.search_st(settings.LDAP_BASE, ldap.SCOPE_SUBTREE, filter, attrlist=attrs, attrsonly=0, timeout=5)
                    if len(r)==0:
                        filter = ldap.filter.filter_format("(sn=%s)",[value])
                        r = self.l.search_st(settings.LDAP_BASE, ldap.SCOPE_SUBTREE, filter, attrlist=attrs, attrsonly=0, timeout=5)
                    if len(r)==0:
                        filter = ldap.filter.filter_format("(uid=%s)",[value])
                        r = self.l.search_st(settings.LDAP_BASE, ldap.SCOPE_SUBTREE, filter, attrlist=attrs, attrsonly=0, timeout=5)
            except ldap.NO_SUCH_OBJECT:
                r = []

            if len(r)==0:
                raise Not_Found_Error("Cannot find DN in LDAP database.")
            elif len(r)>1:
                raise Not_Found_Error("Value not unique LDAP database.")

            return LDAP_Name(r[0])


        def lookup_id(self,value):
            self.open()

            attrs = [ "cn" ]

            try:
                r = self.l.search_st(value, ldap.SCOPE_BASE, filterstr='(objectClass=*)', attrlist=attrs, attrsonly=0, timeout=5)
            except ldap.NO_SUCH_OBJECT:
                r = []

            if len(r)==0:
                raise Not_Found_Error("Cannot find DN in LDAP database.")
            elif len(r)>1:
                raise Lookup_Error("Value not unique LDAP database.")

            return LDAP_Name(r[0])


        def list(self):
            self.open()

            attrs = [ "cn" ]
            list = []

            try:
                r = self.l.search_st(settings.LDAP_PEOPLE, ldap.SCOPE_SUBTREE, filterstr='(objectClass=*)', attrlist=attrs, attrsonly=0, timeout=5)
            except ldap.NO_SUCH_OBJECT:
                r = []

            for n in r[1:]:
                list.append(LDAP_Name(n))

            try:
                r = self.l.search_st(settings.LDAP_GROUPS, ldap.SCOPE_SUBTREE, filterstr='(objectClass=*)', attrlist=attrs, attrsonly=0, timeout=5)
            except ldap.NO_SUCH_OBJECT:
                r = []

            for n in r[1:]:
                list.append(LDAP_Name(n))

            return list


        def close(self):
            if self.l is None:
                return

            self.l.unbind_s()
            self.l = None


def ldap_get(dn,attrlist):
        try:
            l = ldap.initialize(settings.LDAP_URI)
        except ldap.LDAPError:
            raise Lookup_Error("Cannot connect to LDAP server.")

        try:
            r = l.search_st(dn, ldap.SCOPE_BASE, filterstr='(objectClass=*)', attrlist=attrlist, attrsonly=0, timeout=5)
        except ldap.NO_SUCH_OBJECT:
            r = []

        l.unbind_s()

        if len(r)==0:
            raise Lookup_Error("Cannot find DN in LDAP database.")
        elif len(r)>1:
            raise Lookup_Error("Value not unique LDAP database.")

        return r


class LDAP_Name(Name_Base):
    data = None

    def __init__(self,data):
        self.data = data

    def get_id(self):
        return self.data[0]

    def __unicode__(self):
        if self.data[1].has_key("cn"):
                return u"%s"%(self.data[1]["cn"][0])
        else:
                return self.get_dn()

    def is_in_group(self,group):
        r1 = ldap_get(self.get_id(),['objectClass','gidNumber','uid'])
        r2 = ldap_get(group.get_id(),['objectClass','gidNumber','memberUid'])

        if not 'posixAccount' in r1[0][1]['objectClass']:
                return False

        if not 'posixGroup' in r2[0][1]['objectClass']:
                return False

        if r1[0][1]['gidNumber'][0] == r2[0][1]['gidNumber'][0]:
                return True

        if not  r2[0][1].has_key('memberUid'):
                 r2[0][1]['memberUid'] = []

        if r1[0][1].has_key('uid') and r2[0][1].has_key('memberUid'):
                for member in r2[0][1]['memberUid']:
                        if member == r1[0][1]['uid'][0]:
                                return True

        return False
