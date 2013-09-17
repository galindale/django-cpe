# -*- coding: utf-8 -*-

"""
This file is part of django-cpe package.

This module contains the tests to check operations of deprecation elements of
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

from djangocpe.models import DeprecatedBy, Deprecation
from djangocpe.models import DEPRECATED_BY_NAME_CORRECTION
from .fixtures import good_cpedata


@pytest.mark.django_db
class TestDeprecatedBy:
    """
    Tests to check operations with deprecated by elements
    of CPE dictionary model.
    """

    def test_good_deprecatedby(self, good_cpedata):
        """
        Check the creation of a correct deprecated by element.
        """

        # Create element
        good_cpedata.full_clean()
        good_cpedata.save()

        dep = mommy.make(Deprecation)

        dep_type = DEPRECATED_BY_NAME_CORRECTION
        depby = DeprecatedBy(dep_type=dep_type,
                             cpename=good_cpedata,
                             deprecation=dep)
        # Element validation
        depby.full_clean()

        # Save element in database
        depby.save()

        # Load elem from database
        depby_db = DeprecatedBy.objects.get(dep_type=depby.dep_type,
                                            cpename=depby.cpename,
                                            deprecation=depby.deprecation)

        assert depby.id == depby_db.id

    def test_bad_deprecatedby_type(self, good_cpedata):
        """
        Check the creation of a deprecated by elementç
        with an invalid deprecation type.
        """

        # Create element
        good_cpedata.full_clean()
        good_cpedata.save()

        dep = mommy.make(Deprecation)

        dep_type = -1
        depby = DeprecatedBy(dep_type=dep_type,
                             cpename=good_cpedata,
                             deprecation=dep)

        # Element validation
        with pytest.raises(ValidationError) as e:
            depby.full_clean()
        assert 'dep_type' in e.value.message_dict
