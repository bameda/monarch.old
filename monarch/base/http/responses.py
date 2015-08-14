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


from django.http.response import HttpResponseBase
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponsePermanentRedirect
from . import status


class HttpResponse(HttpResponse):
    def __init__(self, content="", *args, **kwarg):
        self.content_data = content
        super(HttpResponse, self).__init__(content, *args, **kwarg)

    @property
    def content_data(self):
        return self.__content_data

    @content_data.setter
    def content_data(self, value):
        self.__content_data = value


class Ok(HttpResponse):
    status_code = status.HTTP_200_OK

class Created(HttpResponse):
    status_code = status.HTTP_201_CREATED

class Accepted(HttpResponse):
    status_code = status.HTTP_202_ACCEPTED

class NoContent(HttpResponse):
    status_code = status.HTTP_204_NO_CONTENT

class MultipleChoices(HttpResponse):
    status_code = status.HTTP_300_MULTIPLE_CHOICES

class MovedPermanently(HttpResponsePermanentRedirect):
    status_code = status.HTTP_301_MOVED_PERMANENTLY

class Redirect(HttpResponseRedirect):
    status_code = status.HTTP_302_FOUND

class SeeOther(HttpResponse):
    status_code = status.HTTP_303_SEE_OTHER

class NotModified(HttpResponse):
    status_code = status.HTTP_304_NOT_MODIFIED

class TemporaryRedirect(HttpResponse):
    status_code = status.HTTP_307_TEMPORARY_REDIRECT

class BadRequest(HttpResponse):
    status_code = status.HTTP_400_BAD_REQUEST

class Unauthorized(HttpResponse):
    status_code = status.HTTP_401_UNAUTHORIZED

class Forbidden(HttpResponse):
    status_code = status.HTTP_403_FORBIDDEN

class NotFound(HttpResponse):
    status_code = status.HTTP_404_NOT_FOUND

class MethodNotAllowed(HttpResponse):
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED

class NotAcceptable(HttpResponse):
    status_code = status.HTTP_406_NOT_ACCEPTABLE

class Conflict(HttpResponse):
    status_code = status.HTTP_409_CONFLICT

class Gone(HttpResponse):
    status_code = status.HTTP_410_GONE

class PreconditionFailed(HttpResponse):
    status_code = status.HTTP_412_PRECONDITION_FAILED

class UnsupportedMediaType(HttpResponse):
    status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE

class TooManyRequests(HttpResponse):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS

class InternalServerError(HttpResponse):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

class NotImplemented(HttpResponse):
    status_code = status.HTTP_501_NOT_IMPLEMENTED

