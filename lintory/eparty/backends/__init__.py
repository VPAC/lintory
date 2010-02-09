from django.core.urlresolvers import reverse

class Names_Base:
        def open(self):
                pass

        def lookup_user_input(self,value):
                raise Lookup_Error("Method not implemented")

        def lookup_id(self,value):
                raise Lookup_Error("Method not implemented")

        def list(self,value):
                raise Lookup_Error("Method not implemented")

        def close(self):
                pass

class Name_Base:
    def get_id(self):
        return None

#    def get_absolute_url(self):
#        return reverse("eparty_detail",kwargs={'object_id': self.get_id()})

    def is_in_group(self,group):
        raise Lookup_Error("Method not implemented")

    def compare(self,object):
        if (self.get_id() == object.get_id()):
                return True
        else:
                return False

    def __unicode__(self):
        return u"%s"%(self.get_id())


class Not_Found_Error(Exception):
        def __init__(self, value):
                self.value = value

        def __str__(self):
                return repr(self.value)

        def __unicode__(self):
                return u"%s"%(self.value)

class Lookup_Error(Exception):
        def __init__(self, value):
                self.value = value

        def __str__(self):
                return repr(self.value)

        def __unicode__(self):
                return u"%s"%(self.value)
