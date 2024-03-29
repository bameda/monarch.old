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


import traceback
import inspect

from django.conf import settings
from django.utils import six
from django.utils.functional import Promise
from django.views.decorators.csrf import csrf_exempt

from ..http import exceptions as exc
from ..http import negotiation
from ..http import responses as res
from ..http import serializers
from ..utils import json


class ApiMixin(object):
    serializers = None

    def __init__(self, *args, **kwarg):
        super(ApiMixin, self).__init__(*args, **kwarg)

        # Set default ones
        if self.serializers is None:
            self.serializers = [serializers.Json(),
                                serializers.HtmlJson()]

        if isinstance(self.serializers, (list, tuple)):
            _serializers = []

            for serializer in self.serializers:
                if isinstance(serializer, six.string_types):
                    _serializers.append(serializers.resolve_by_name(serializer))
                elif inspect.isclass(serializer):
                    _serializers.append(serializer())
                elif isinstance(serializer, serializers.Serializer):
                    _serializers.append(serializer)
                else:
                    raise RuntimeException("Invalid serializers.")

            self.serializers = serializers.SerializersContainer(*_serializers)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        response_content_type = self.serializers.get_default_content_type()

        try:
            content_type = request.META.get("CONTENT_TYPE", response_content_type)
            content_length = request.META.get("CONTENT_LENGTH", "")

            if content_length:
                content_type_serializer = self.serializers.get_by_content_type(content_type)
                if content_type_serializer is None:
                    raise exc.UnsupportedMediaType("Unsupported Media Type.")
                else:
                    request.data = content_type_serializer.loads(request)

            media_types = negotiation.parse_media_range(request.META.get("HTTP_ACCEPT", "*/*"))
            serializers_media_range = ",".join(s.content_type for s in self.serializers)
            serializers_media_types = negotiation.parse_media_range(serializers_media_range)
            media_type = negotiation.intersect_media_types(media_types, serializers_media_types)
            if media_type is None:
                raise exceptions.NotAcceptable()

            response_content_type = str(media_type)
            response = super(ApiMixin, self).dispatch(request, *args, **kwargs)
        except exc.BaseException as e:
            if isinstance(e.content, six.string_types + (Promise,)):
                response = e.response_class({"_message": e.content})
            else:
                response = e.response_class(e.content)

        serializer = self.serializers.get_by_content_type(response_content_type)
        if isinstance(response, res.HttpResponse):
            response.content = serializer.dumps(response.content_data, request, response)

        return response
