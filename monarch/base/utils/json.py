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


import datetime
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.utils.functional import Promise
from django.utils import timezone

from django.utils.encoding import force_str


class LazyEncoder(DjangoJSONEncoder):
    """
    JSON encoder class for encode correctly traduction strings.
    Is for ajax response encode.
    """
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_str(obj)
        elif isinstance(obj, datetime.datetime):
            obj = timezone.localtime(obj)
        return super(LazyEncoder, self).default(obj)


def dumps(data, ensure_ascii=True, cls=LazyEncoder, **kwargs):
    return json.dumps(data, cls=cls, ensure_ascii=ensure_ascii, **kwargs)


def loads(data):
    return json.loads(data)
