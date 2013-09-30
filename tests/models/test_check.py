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

    def test_good_check_min_fields(self):
        """
        Check the creation of a correct check element
        with only required fields filled.
        """

        # Create check element
        cpeitem = mommy.make(CpeItem)
        check = mommy.prepare(Check,
            system="http://oval.mitre.org/XMLSchema/oval-definitions-5",
            cpeitem=cpeitem)

        # Element validation
        check.full_clean()

        # Save element in database
        check.save()

        # Load element from database
        check_db = Check.objects.get(check_id=check.check_id,
                                     system=check.system)

        assert check.id == check_db.id
        assert check.check_id == check_db.check_id
        assert check.href == check_db.href
        assert check.system == check_db.system

    def test_good_check_all_fields(self):
        """
        Check the creation of a correct check element
        with all fields filled.
        """

        # Create check element
        cpeitem = mommy.make(CpeItem)
        check = mommy.prepare(Check,
            href="http://oval.mitre.gov",
            system="http://oval.mitre.org/XMLSchema/oval-definitions-5",
            cpeitem=cpeitem)

        # Element validation
        check.full_clean()

        # Save element in database
        check.save()

        # Load element from database
        check_db = Check.objects.get(check_id=check.check_id,
                                     href=check.href,
                                     system=check.system)

        assert check.id == check_db.id
        assert check.check_id == check_db.check_id
        assert check.href == check_db.href
        assert check.system == check_db.system

    def test_bad_check_ref(self):
        """
        Check the creation of a check element with an invalid
        file reference value.
        """

        # TODO: test urn in system_uri, e. g., urn:ietf:rfc:2648
        cpeitem = mommy.make(CpeItem)
        check = mommy.prepare(Check,
            href="baduri",
            system="http://oval.mitre.org",
            cpeitem=cpeitem)

        with pytest.raises(ValidationError) as e:
            check.full_clean()

        assert 'href' in e.value.message_dict
        assert 'system_uri' not in e.value.message_dict

    def test_bad_check_system(self):
        """
        Check the creation of a check element with an invalid
        system value.
        """

        # TODO: test urn in file_ref, e. g., urn:ietf:rfc:2648
        cpeitem = mommy.make(CpeItem)
        check = mommy.prepare(Check,
            href="http://oval.mitre.org",
            system="baduri",
            cpeitem=cpeitem)

        with pytest.raises(ValidationError) as e:
            check.full_clean()

        assert 'href' not in e.value.message_dict
        assert 'system' in e.value.message_dict
