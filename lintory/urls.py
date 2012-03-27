# lintory - keep track of computers and licenses
# Copyright (C) 2008-2009 Brian May
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls.defaults import url, include, patterns
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',
    'lintory.views.root',
    name='root'),


    url(r'^vendor/$',
    'lintory.views.vendor_list',
    name="vendor_list"),

    url(r'^vendor/(?P<object_id>\d+)/$',
    'lintory.views.vendor_detail',
    name='vendor_detail'),

    url(r'^vendor/add/$',
    'lintory.views.vendor_add',
    name='vendor_add'),

    url(r'^vendor/(?P<object_id>\d+)/edit/$',
    'lintory.views.vendor_edit',
    name='vendor_edit'),

    url(r'^vendor/(?P<object_id>\d+)/delete/$',
    'lintory.views.vendor_delete',
    name='vendor_delete'),


    url(r'^party/$',
    'lintory.views.party_list',
    name='party_list'),

    url(r'^party/(?P<object_id>\d+|none)/$',
    'lintory.views.party_detail',
    name='party_detail'),

    url(r'^party/add/$',
    'lintory.views.party_add',
    name='party_add'),

    url(r'^party/(?P<object_id>\d+)/edit/$',
    'lintory.views.party_edit',
    name='party_edit'),

    url(r'^party/(?P<object_id>\d+)/delete/$',
    'lintory.views.party_delete',
    name='party_delete'),

    url(r'^party/(?P<object_id>\d+|none)/software/$',
    'lintory.views.party_software_list',
    name='party_software_list'),

    url(r'^party/(?P<object_id>\d+|none)/software/(?P<software_id>\d+)/$',
    'lintory.views.party_software_detail',
    name='party_software_detail'),


    url(r'^(?P<type_id>\w+)/(?P<object_id>\d+)/history/add/$',
    'lintory.views.history_item_add',
    name='history_item_add'),

    url(r'^history/(?P<history_item_id>\d+)/edit/$',
    'lintory.views.history_item_edit',
    name='history_item_edit'),

    url(r'^history/(?P<history_item_id>\d+)/delete/$',
    'lintory.views.history_item_delete',
    name='history_item_delete'),

    url(r'^task/$',
    'lintory.views.task_list',
    name='task_list'),

    url(r'^task/(?P<object_id>\d+)/$',
    'lintory.views.task_detail',
    name='task_detail'),

    url(r'^task/add/$',
    'lintory.views.task_add',
    name='task_add'),

    url(r'^task/(?P<object_id>\d+)/edit/$',
    'lintory.views.task_edit',
    name='task_edit'),

    url(r'^task/(?P<object_id>\d+)/delete/$',
    'lintory.views.task_delete',
    name='task_delete'),

    url(r'^task/(?P<object_id>\d+)/add_hardware/$',
    'lintory.views.task_add_hardware',
    name='task_add_hardware'),

    url(r'^hardware_task/(?P<object_id>\d+)/edit/$',
    'lintory.views.hardware_task_edit',
    name='hardware_task_edit'),

    url(r'^hardware_task/(?P<object_id>\d+)/delete/$',
    'lintory.views.hardware_task_delete',
    name='hardware_task_delete'),


    (r'^location/$',
    'lintory.views.location_redirect',
    {'object_id': 1}),

    url(r'^location/(?P<object_id>\d+)/$',
    'lintory.views.location_detail',
    name='location_detail'),

    url(r'^location/(?P<object_id>\d+)/tasks/$',
    'lintory.views.location_task_list',
    name='location_task_list'),

    url(r'^location/(?P<object_id>\d+)/tasks/(?P<task_id>\d+)/$',
    'lintory.views.location_task',
    name='location_task'),

    url(r'^location/(?P<object_id>\d+)/add/$',
    'lintory.views.location_add',
    name='location_add'),

    url(r'^location/(?P<object_id>\d+)/edit/$',
    'lintory.views.location_edit',
    name='location_edit'),

    url(r'^location/(?P<object_id>\d+)/delete/$',
    'lintory.views.location_delete',
    name='location_delete'),

    url(r'^location/(?P<object_id>\d+).svg$',
    'lintory.views.location_svg',
    name='location_svg'),


    url(r'^license/$',
    'lintory.views.license_list',
    name='license_list'),

    url(r'^license/(?P<object_id>\d+)/$',
    'lintory.views.license_detail',
    name='license_detail'),

    url(r'^license/add/$',
    'lintory.views.license_add',
    name='license_add'),

    url(r'^license/(?P<object_id>\d+)/edit/$',
    'lintory.views.license_edit',
    name='license_edit'),

    url(r'^license/(?P<object_id>\d+)/delete/$',
    'lintory.views.license_delete',
    name='license_delete'),

    url(r'^license/(?P<object_id>\d+)/add_license_key/$',
    'lintory.views.license_add_license_key',
    name='license_add_license_key'),


    url(r'^license_key/(?P<object_id>\d+)/$',
    'lintory.views.license_key_detail',
    name='license_key_detail'),

    url(r'^license_key/(?P<object_id>\d+)/edit/$',
    'lintory.views.license_key_edit',
    name='license_key_edit'),

    url(r'^license_key/(?P<object_id>\d+)/delete/$',
    'lintory.views.license_key_delete',
    name='license_key_delete'),


    url(r'^software/$',
    'lintory.views.software_list',
    name='software_list'),

    url(r'^software/(?P<object_id>\d+)/$',
    'lintory.views.software_detail',
    name='software_detail'),

    url(r'^software/add/$',
    'lintory.views.software_add',
    name='software_add'),

    url(r'^software/(?P<object_id>\d+)/edit/$',
    'lintory.views.software_edit',
    name='software_edit'),

    url(r'^software/(?P<object_id>\d+)/delete/$',
    'lintory.views.software_delete',
    name='software_delete'),

    url(r'^software/(?P<object_id>\d+)/add_software_installation/$',
    'lintory.views.software_add_software_installation',
    name='software_add_software_installation'),

    url(r'^software/(?P<object_id>\d+)/add_license/$',
    'lintory.views.software_add_license',
    name='software_add_license'),

    url(r'^software_installation/(?P<object_id>\d+)/edit/$',
    'lintory.views.software_installation_edit',
    name='software_installation_edit'),

    url(r'^software_installation/(?P<object_id>\d+)/edit_license_key/$',
    'lintory.views.software_installation_edit_license_key',
    name='software_installation_edit_license_key'),

    url(r'^software_installation/(?P<object_id>\d+)/delete/$',
    'lintory.views.software_installation_delete',
    name='software_installation_delete'),


    url(r'^hardware/$',
    'lintory.views.hardware_list',
    name='hardware_list'),

    url(r'^hardware/(?P<object_id>\d+)/$',
    'lintory.views.hardware_detail',
    name='hardware_detail'),

    url(r'^hardware/add/$',
    'lintory.views.hardware_add',
    name='hardware_add'),

    url(r'^hardware/add/(?P<type_id>\w+)/$',
    'lintory.views.hardware_type_add',
    name='hardware_type_add'),

    url(r'^hardware/(?P<object_id>\d+)/edit/$',
    'lintory.views.hardware_edit',
    name='hardware_edit'),

    url(r'^hardware/(?P<object_id>\d+)/install/$',
    'lintory.views.hardware_install',
    name='hardware_install'),

    url(r'^hardware/(?P<object_id>\d+)/add/$',
    'lintory.views.hardware_add',
    name='hardware_add'),

    url(r'^hardware/(?P<object_id>\d+)/add/(?P<type_id>\w+)/$',
    'lintory.views.hardware_type_add',
    name='hardware_add'),

    url(r'^hardware/(?P<object_id>\d+)/delete/$',
    'lintory.views.hardware_delete',
    name='hardware_delete'),


    url(r'^os/(?P<object_id>\d+)/$',
    'lintory.views.os_detail',
    name='os_detail'),

    url(r'^hardware/(?P<object_id>\d+)/os/add/$',
    'lintory.views.os_add',
    name='os_add'),

    url(r'^os/(?P<object_id>\d+)/edit/$',
    'lintory.views.os_edit',
    name='os_edit'),

    url(r'^os/(?P<object_id>\d+)/delete/$',
    'lintory.views.os_delete',
    name='os_delete'),

    url(r'^upload/windows/lintory.txt$',
    'lintory.upload.windows.upload',
    name='windows_upload'),


    url(r'^data/$',
    'lintory.views.data_list',
    name="data_list"),

    url(r'^data/(?P<object_id>\d+)/$',
    'lintory.views.data_detail',
    name='data_detail'),

    url(r'^data/add/$',
    'lintory.views.data_add',
    name='data_add'),

    url(r'^data/(?P<object_id>\d+)/edit/$',
    'lintory.views.data_edit',
    name='data_edit'),

    url(r'^data/(?P<object_id>\d+)/delete/$',
    'lintory.views.data_delete',
    name='data_delete'),


    url(r'^ajax/', include('ajax_select.urls')),

    # account management
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^account/logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^account/password_change/$', 'django.contrib.auth.views.password_change', name='password_change'),
    url(r'^account/password_change/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
