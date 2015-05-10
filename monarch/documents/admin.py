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


from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("subject", ("author", "creation_date"))}),
        (_("Info"), {"fields": ("file", "description", )}),
    )
    list_display = ("id", "subject", "author", "creation_date")
    list_filter = ("creation_date",)
    search_fields = ("subject", "description",  "author__email", "author__username", "author__full_name")
    ordering = ("-creation_date",)

