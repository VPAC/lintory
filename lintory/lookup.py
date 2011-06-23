from lintory import models
from django.db.models import Q
from django.utils.html import escape
from django.conf import settings


class party_lookup(object):

    def get_query(self,q,request):
        """ return a query set.  you also have access to request.user if needed """
        return models.party.objects.filter(name__icontains=q)

    def format_item(self,object):
        """ simple display of an object when it is displayed in the list of selected objects """
        return escape(unicode(object))

    def format_result(self,object):
        """ a more verbose display, used in the search results display.  may contain html and multi-lines """
        return u"%s"%(escape(object))

    def get_objects(self,ids):
        """ given a list of ids, return the objects ordered as you would like them on the admin page.
            this is for displaying the currently selected items (in the case of a ManyToMany field)
        """
        result=[]
        for id in ids:
                result.append(models.party.objects.get(pk=id))
        return result

class location_lookup(object):

    def get_query(self,q,request):
        """ return a query set.  you also have access to request.user if needed """
        return models.location.objects.filter(Q(name__icontains=q))

    def format_item(self,object):
        """ simple display of an object when it is displayed in the list of selected objects """
        return escape(unicode(object))

    def format_result(self,object):
        """ a more verbose display, used in the search results display.  may contain html and multi-lines """
        return u"%s"%(escape(object))

    def get_objects(self,ids):
        """ given a list of ids, return the objects ordered as you would like them on the admin page.
            this is for displaying the currently selected items (in the case of a ManyToMany field)
        """
        return models.location.objects.filter(pk__in=ids)

class software_lookup(object):

    def get_query(self,q,request):
        """ return a query set.  you also have access to request.user if needed """
        return models.software.objects.filter(name__icontains=q)

    def format_item(self,object):
        """ simple display of an object when it is displayed in the list of selected objects """
        return escape(unicode(object))

    def format_result(self,object):
        """ a more verbose display, used in the search results display.  may contain html and multi-lines """
        return u"%s"%(escape(object))

    def get_objects(self,ids):
        """ given a list of ids, return the objects ordered as you would like them on the admin page.
            this is for displaying the currently selected items (in the case of a ManyToMany field)
        """
        result=[]
        for id in ids:
                result.append(models.software.objects.get(pk=id))
        return result

