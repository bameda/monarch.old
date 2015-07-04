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


from contextlib import contextmanager

from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.utils.translation import ugettext_lazy as _
from django.http import Http404
from django.db import IntegrityError


from . import responses


class BaseException(Exception):
    default_content = _("Unexpected error")
    response_class = responses.BadRequest

    def __init__(self, detail=None):
        self.content = detail or self.default_content


class UnsupportedMediaType(BaseException):
    response_class = responses.UnsupportedMediaType


class MethodNotAllowed(BaseException):
    response_class = responses.MethodNotAllowed


class NotAcceptable(BaseException):
    response_class = responses.NotAcceptable


class NotFound(BaseException, Http404):
    default_content = _("Not found.")
    response_class = responses.NotFound


class Forbidden(BaseException, DjangoPermissionDenied):
    response_class = responses.Forbidden
    default_content = _("Permission denied")


class Unauthorized(BaseException):
    response_class = responses.Unauthorized


class BadRequest(BaseException):
    pass


class WrongArguments(BadRequest):
    default_content = _("Wrong arguments.")


class ValidationError(BadRequest):
    default_content = _("Data validation error")


class Redirect(BaseException):
    response_class = responses.TemporaryRedirect


class RedirectPermanent(BaseException):
    response_class = responses.MovedPermanently


class IntegrityError(BaseException):
    default_content = _("Integrity Error for wrong or invalid arguments")
    response_class = responses.Conflict


class InternalError(BaseException):
    default_content = _("Internal server error")
    response_class = responses.InternalServerError


@contextmanager
def supress_exceptions(*exceptions):
    """
    Util context manager for avoid empty
    try/except:pass blocks and put them in more
    idiomatic code.
    """
    try:
        yield
    except exceptions as e:
        pass

