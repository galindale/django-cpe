# -*- coding: utf-8 -*-

"""
This file is part of django-cpe package.

This module contains the tests to check operations of organization elements of
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

from django.utils import timezone
from django.core.exceptions import ValidationError
from model_mommy import mommy

from djangocpe.models import Organization


@pytest.mark.django_db
class TestOrganization:
    """
    Tests to check operations with organization elements
    of CPE dictionary model.
    """

    def test_good_org(self):
        """
        Check the creation of a correct organization element.
        """

        # Create values
        suri = "http://cpe.mitre.org"
        name = "Mitre Corporation"
        dt = timezone.now()
        desc = "This organization supports the CPE specification"

        # Save elem in database
        org = Organization(system_uri=suri,
                           name=name,
                           datetime_action=dt,
                           description=desc)
        org.full_clean(['description'])
        org.save()

        # Load elem from database
        org_db = Organization.objects.get(system_uri=suri,
                                          name=name,
                                          datetime_action=dt,
                                          description=desc)
        # Compare values
        assert suri == org_db.system_uri
        assert name == org_db.name
        # TODO: investigate datetime comparison
        #assert dt == org_db.datetime_action
        assert desc == org_db.description

    def test_bad_org_uri_value(self):
        """
        Check the creation of an organization with an invalid
        system uri value.
        """

        org = mommy.prepare(Organization, system_uri="baduri")

        with pytest.raises(ValidationError):
            org.full_clean(['description'])

    def test_bad_org_uri_length(self):
        """
        Check the creation of an organization with an invalid
        system uri value.
        """

        org = mommy.prepare(Organization, system_uri=("u" * 256))
        with pytest.raises(ValidationError):
            org.full_clean(['description'])
