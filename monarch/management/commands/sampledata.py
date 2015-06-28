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

from django.core.management.base import BaseCommand
from django.db import transaction
import logging


from sampledatahelper.helper import SampleDataHelper

from monarch.users.models import User

log = logging.getLogger(__name__)


NUM_USERS = 10

class Command(BaseCommand):
    sd = SampleDataHelper(seed=12345678901)

    @transaction.atomic
    def handle(self, *args, **options):
        self._create_admin_user()

        for i in range(1, NUM_USERS+1):
            self._create_user(i)

    def _create_admin_user(self):
        username = "admin"
        email = "admin@monarch.com"
        full_name = "Administrator"

        user, created = User.objects.get_or_create(username=username,
                                                   email=email,
                                                   defaults={"full_name": full_name})

        if created:
            user.set_password("123123")
            user.save()

        if not created:
            log.warning(" -!- 'admin' user exist")

        return user

    def _create_user(self, idx):
        username = "user{}".format(idx)
        email = "user{}@admin.com".format(idx)
        full_name = "{} {}".format(self.sd.name("es"), self.sd.surname("es", number=1))

        user, created = User.objects.get_or_create(username=username,
                                                   email=email,
                                                   defaults={"full_name": full_name})

        if created:
            user.set_password("123123")
            user.save()

        if not created:
            log.warning(" -!- '{}' user exist".format(username))

        return user
