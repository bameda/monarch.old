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


from django.core.urlresolvers import reverse
from django.views.generic import View as DjangoView
from django.template.loader import render_to_string, get_template

from monarch.base.http import responses as res
from monarch.base.http import exceptions as exc


class View(DjangoView):
    response_cls = res.Ok
    content_type = "text/html"
    permissions = ()

    def handle_exception(self, e):
        """
        Ad-hoc exception handling for all derived views.
        """
        if isinstance(e, exc.Redirect):
            return e.response_class(headers={"Location": e.content})
        elif isinstance(e, exc.RedirectPermanent):
            return e.response_class(headers={"Location": e.content})
        elif isinstance(e, exc.IntegrityError):
            return e.response_class(e.content)
        elif isinstance(e, exc.MethodNotAllowed):
            return e.response_class(headers={"Allow": e.content})
        return e

    def init(self, request, *args, **kwargs):
        pass

    def get_context_data(self):
        context = {"view": self}
        context.update(self.kwargs)
        return context

    def __handle_permissions(self):
        for fn in self.permissions:
            result = fn(self)
            if isinstance(result, res.HttpResponseBase):
                return result
            elif result == False:
                raise exc.PermissionDenied("Forbidden")

        if hasattr(self, "handle_permissions"):
            return self.handle_permissions()

    def dispatch(self, request, *args, **kwargs):
        try:
            result = self.init(request, *args, **kwargs)
            if isinstance(result, res.HttpResponseBase):
                return result
            result = self.__handle_permissions()
            if isinstance(result, res.HttpResponseBase):
                return result
            return super(View, self).dispatch(request, *args, **kwargs)
        except Exception as e:
            response = self.handle_exception(e)
            if isinstance(response, Exception):
                raise
            return response

    def redirect(self, reverseurl=None, url=None, args=None, kwargs=None):
        """
        Simple redirect helper.
        """
        if not url:
            url = reverse(reverseurl, args=args, kwargs=kwargs)
        return res.Redirect(url)

    def render(self, template=None, context=None, data=None,
               response_cls=None, content_type=None, status_code=None):
        output_data = data or b""

        if template:
            _context = self.get_context_data()
            _context.update(context or {})

            template = get_template(template)
            output_data = template.render(_context, request=self.request)

        if content_type is None:
            content_type = self.content_type

        if not response_cls:
            response_cls = self.response_cls

        response = response_cls(output_data, content_type=content_type)
        if status_code:
            response.status_code = status_code

        return response


class TemplateView(View):
    tmpl_name = None

    def get(self, request, *args, **kwargs):
        if self.tmpl_name is None:
            raise ValueError("tmpl_name attr must be a valid template name")
        return self.render(self.tmpl_name)
