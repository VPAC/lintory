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

from django.core.management.base import BaseCommand, CommandError

from optparse import make_option
import os
import datetime

from lintory.upload.windows import load
from lintory import models

from django.conf import settings

class Command(BaseCommand):
        args = '<file file ...>'
        help = 'Imports data records into lintory'
        option_list = BaseCommand.option_list + (
            make_option('-d', '--delete_old',
                action='store_true',
                dest='delete',
                default=False,
                help='Delete old/obsolete records'),
            make_option('-r', '--redo',
                action='store_true',
                dest='redo',
                default=False,
                help='Import latest data files with known computer even if already imported'),
            )

        def handle(self, *args, **options):
            if options['redo']:
                # only redo latest record for every computer
                for computer in models.computer.objects.all():
                    data_list = models.data.objects.filter(computer=computer, format="windows").order_by("-datetime")
                    try:
                        data = data_list[0]
                        print "--- %s (%d) ---"%(data.file, data.pk)
                        load(data)
                        print
                    except IndexError, e:
                        pass

            if options['delete']:
                # no point keeping old records where known newer record exists
                for computer in models.computer.objects.all():
                    data_list = models.data.objects.filter(computer=computer, format="windows").order_by("datetime")
                    last = None
                    for data in data_list:
                        if last is not None:
                            last.delete()
                        last = data

                # records older then 180 days are so old they are useless
                data_list = models.data.objects.filter(datetime__lt=datetime.datetime.now() - datetime.timedelta(days=180))
                for data in data_list:
                    data.delete()

            for data in models.data.objects.filter(imported__isnull=True, format="windows"):
                print "--- %s (%d) ---"%(data.file, data.pk)
                load(data)
                print

            for arg in args:
                path = os.path.realpath(arg)
                modified = os.path.getmtime(path)
                data_datetime = datetime.datetime.fromtimestamp(modified)
                data_datetime = data_datetime.replace(microsecond=0)

                # Is this path in the upload directory?
                (head,tail) = os.path.split(path)
                while head != "" and head != "/" and head!=settings.UPLOAD_DIR:
                    (head,new_tail) = os.path.split(head)
                    tail = os.path.join(new_tail,tail)

                # If this path was in the upload directory, see if we can find it
                # in database
                data=None
                if head!="" and head!="/":
                    try:
                        data = models.data.objects.get(file=tail)
                    except models.data.DoesNotExist, e:
                        pass

                # If we can't find entry in database, we need to create entry
                if data is None:
                    data = models.data()
                    data.datetime = data_datetime
                    data.format = "windows"

                # Do we need to rename this file?
                data.file = models.data_upload_to(data, None)
                if os.path.exists(data.file.path):
                    if not os.path.samefile(path, data.file.path):
                        raise CommandError("Destination '%s' already exists"%(data.file.path))
                    else:
                        # File is the same, no need to rename it.
                        pass
                else:
                    # Rename file to our standard (won't work across file systems)
                    print "Renaming '%s' to '%s'"%(path,data.file.path)

                    (head,tail) = os.path.split(data.file.path)
                    if not os.path.exists(head):
                        os.makedirs(head)

                    os.rename(path, data.file.path)

                # Save data
                data.save()

                # Load data into database
                load(data)

            return 0
