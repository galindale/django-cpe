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

    def test_good_org_min_fields(self):
        """
        Check the creation of a correct organization element
        with only required fields filled.
        """

        # Create organization element
        suri = "http://cpe.mitre.org"
        name = "Mitre Corporation"
        dt = timezone.now()

        org = Organization(system_id=suri,
                           name=name,
                           action_datetime=dt)

        # Element validation
        org.full_clean()

        # Save element in database
        org.save()

        # Load element from database
        org_db = Organization.objects.get(system_id=org.system_id,
                                          name=org.name,
                                          action_datetime=org.action_datetime)
        # Compare values
        assert org.id == org_db.id
        assert org.system_id == org_db.system_id
        assert org.name == org_db.name
        assert org.action_datetime == org_db.action_datetime
        assert org.description == org_db.description

    def test_good_org_all_fields(self):
        """
        Check the creation of a correct organization element
        with all fields filled.
        """

        # Create organization element
        suri = "http://cpe.mitre.org"
        name = "Mitre Corporation"
        dt = timezone.now()
        desc = "This organization supports the CPE specification"

        org = Organization(system_id=suri,
                           name=name,
                           action_datetime=dt,
                           description=desc)

        # Element validation
        org.full_clean()

        # Save element in database
        org.save()

        # Load element from database
        org_db = Organization.objects.get(system_id=org.system_id,
                                          name=org.name,
                                          action_datetime=org.action_datetime,
                                          description=org.description)
        # Compare values
        assert org.id == org_db.id
        assert org.system_id == org_db.system_id
        assert org.name == org_db.name
        assert org.action_datetime == org_db.action_datetime
        assert org.description == org_db.description

    def test_bad_org_systemid(self):
        """
        Check the creation of an organization with an invalid
        system id value.
        """

        org = mommy.prepare(Organization, system_id="baduri")

        with pytest.raises(ValidationError) as e:
            org.full_clean()

        assert 'system_id' in e.value.message_dict
