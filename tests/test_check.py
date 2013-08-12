# -*- coding: utf-8 -*-

"""
This file is part of django-cpe package.

This module contains the tests to check operations of check elements of
CPE dictionary model.

Copyright (C) 2013  Alejandro Galindo García, Roberto Abdelkader Martínez Pérez

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

For any problems using the django-cpe package, or general questions and
feedback about it, please contact:

- Alejandro Galindo García: galindo.garcia.alejandro@gmail.com
- Roberto Abdelkader Martínez Pérez: robertomartinezp@gmail.com
"""

import pytest

from django.core.exceptions import ValidationError
from model_mommy import mommy

from djangocpe.models import Check, CpeItem


@pytest.mark.django_db
class TestCheck:
    """
    Tests to check operations with check elements
    of CPE dictionary model.
    """

    def test_good_check(self):
        """
        Check the creation of a correct check element.
        """

        # Create check element in database
        cpeitem = mommy.make(CpeItem)
        check = mommy.prepare(Check,
                              file_ref="http://www.nist.gov",
                              system_uri="http://oval.mitre.org",
                              cpeitem=cpeitem)

        # Object validation
        check.full_clean(['description'])
        check.save()

        # Load elem from database
        check_db = Check.objects.get(file_ref=check.file_ref,
                                     system_uri=check.system_uri)

        assert check.id == check_db.id

    def test_bad_check_file_ref(self):
        """
        Check the creation of a check element with an invalid
        file reference value.
        """

        # TODO: test urn in system_uri, e. g., urn:ietf:rfc:2648
        cpeitem = mommy.make(CpeItem)
        check = mommy.prepare(Check,
                              file_ref="baduri",
                              system_uri="http://oval.mitre.org",
                              cpeitem=cpeitem)

        with pytest.raises(ValidationError) as e:
            check.full_clean(['description'])

        e_str = str(e.value)

        assert 'file_ref' in e.value.message_dict
        assert 'system_uri' not in e.value.message_dict

    def test_bad_check_system_uri(self):
        """
        Check the creation of a check element with an invalid
        system uri value.
        """

        # TODO: test urn in file_ref, e. g., urn:ietf:rfc:2648
        cpeitem = mommy.make(CpeItem)
        check = mommy.prepare(Check,
                              file_ref="http://oval.mitre.org",
                              system_uri="baduri",
                              cpeitem=cpeitem)

        with pytest.raises(ValidationError) as e:
            check.full_clean(['description'])

        e_str = str(e.value)

        assert 'file_ref' not in e.value.message_dict
        assert 'system_uri' in e.value.message_dict
