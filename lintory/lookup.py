from lintory import models
from django.db.models import Q
from django.utils.html import escape
from django.conf import settings
from ajax_select import LookupChannel

class LookupChannel(LookupChannel):
    # anyone can use these lookup methods
    def check_auth(self, request):
        return

class party_lookup(LookupChannel):

    def get_query(self,q,request):
        """ return a query set.  you also have access to request.user if needed """
        return models.party.objects.filter(name__icontains=q)

    def format_item_display(self,object):
        """ simple display of an object when it is displayed in the list of selected objects """
        return escape(unicode(object))

    def format_match(self,object):
        """ (HTML) formatted item for display in the dropdown """
        return u"%s"%(escape(object))

    def get_objects(self,ids):
        """ given a list of ids, return the objects ordered as you would like them on the admin page.
            this is for displaying the currently selected items (in the case of a ManyToMany field)
        """
        result=[]
        for id in ids:
                result.append(models.party.objects.get(pk=id))
        return result

class location_lookup(LookupChannel):

    def get_query(self,q,request):
        """ return a query set.  you also have access to request.user if needed """
        return models.location.objects.filter(Q(name__icontains=q))

    def format_item_display(self,object):
        """ simple display of an object when it is displayed in the list of selected objects """
        return escape(unicode(object))

    def format_match(self,object):
        """ (HTML) formatted item for display in the dropdown """
        return u"%s"%(escape(object))

    def get_objects(self,ids):
        """ given a list of ids, return the objects ordered as you would like them on the admin page.
            this is for displaying the currently selected items (in the case of a ManyToMany field)
        """
        return models.location.objects.filter(pk__in=ids)

class software_lookup(LookupChannel):

    def get_query(self,q,request):
        """ return a query set.  you also have access to request.user if needed """
        return models.software.objects.filter(name__icontains=q)

    def format_item_display(self,object):
        """ simple display of an object when it is displayed in the list of selected objects """
        return escape(unicode(object))

    def format_match(self,object):
        """ (HTML) formatted item for display in the dropdown """
        return u"%s"%(escape(object))

    def get_objects(self,ids):
        """ given a list of ids, return the objects ordered as you would like them on the admin page.
            this is for displaying the currently selected items (in the case of a ManyToMany field)
        """
        result=[]
        for id in ids:
                result.append(models.software.objects.get(pk=id))
        return result

