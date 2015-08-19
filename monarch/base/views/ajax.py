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

from monarch.base.utils import json

from monarch.base.http import status
from monarch.base.http import exceptions as exc


class AjaxMixin:
    def handle_exception(self, exception):
        """
        Ad-hoc exception handling for all derived views.
        """
        ctx = {"_error": str(exception)}

        if isinstance(exception, exc.WrongArguments):
            return self.render_json(ctx,  status_code=status.HTTP_400_BAD_REQUEST)

        return super().handle_exception(exception)

    def render_json(self, data, content_type=None, status_code=None):
        if content_type is None:
            content_type = "application/json"

        return self.render(data=json.dumps(data),
                           content_type=content_type,
                           status_code=status_code)


