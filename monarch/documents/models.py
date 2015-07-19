# Copyright (C) 2015 David Barragán <bameda@dbarragan.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from django.db import models
from django.utils.translation import ugettext_lazy as _


def calculate_document_path(instance, filename):
    return 'documents/{filename}'.format(filename=filename)


class Document(models.Model):
    subject = models.CharField(null=False, blank=False, max_length=256,
                               verbose_name=_("subject"))
    author = models.CharField(null=False, blank=False, max_length=256,
                              verbose_name=_("author"))
    creation_date = models.DateTimeField(null=False, blank=False, auto_now_add=True,
                                         verbose_name=_("creation date"))
    last_modified_date = models.DateTimeField(null=False, blank=False, auto_now=True,
                                              verbose_name=_("last modified date"))
    description =models.TextField(null=True, blank=True,
                                  verbose_name=_("sdescription"))
    file = models.FileField(null=False, blank=False, upload_to=calculate_document_path,
                            verbose_name=_("file"))

    class Meta:
        verbose_name = "document"
        verbose_name_plural = "documents"
