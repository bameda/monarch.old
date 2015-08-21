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


from monarch.base.http import exceptions as exc

class FormViewMixin(object):
    # Simple heleprs for dealing with forms

    def get_form_cls(self):
        if not hasattr(self, "form_cls"):
            raise exc.InternalError("form_cls attribute not defined")
        return self.form_cls

    def get_form(self, initial=None, **kwargs):
        form_cls = self.get_form_cls()
        if self.request.method == "POST":
            return form_cls(self.request.POST, self.request.FILES, initial=initial, **kwargs)
        return form_cls(initial=initial, **kwargs)
