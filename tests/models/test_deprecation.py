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

from django.utils import timezone
from model_mommy import mommy

from djangocpe.models import Deprecation, CpeItem


@pytest.mark.django_db
class TestDeprecation:
    """
    Tests to check operations with deprecation elements
    of CPE dictionary model.
    """

    def test_good_deprecation_min_fields(self):
        """
        Check the creation of a correct deprecation element
        with only required fields filled.
        """

        # Create deprecation element
        cpeitem = mommy.make(CpeItem)
        depre = Deprecation(cpeitem=cpeitem)

        # Save element in database
        depre.save()

        # Load elem from database
        depre_db = Deprecation.objects.get(cpeitem=depre.cpeitem)

        # Compare values
        assert depre.id == depre_db.id
        assert depre.dep_datetime == depre_db.dep_datetime
        assert depre.cpeitem == depre_db.cpeitem

    def test_good_deprecation_all_fields(self):
        """
        Check the creation of a correct deprecation element
        with all fields filled.
        """

        # Create deprecation element
        cpeitem = mommy.make(CpeItem)
        dt = timezone.now()
        depre = Deprecation(dep_datetime=dt, cpeitem=cpeitem)

        # Save element in database
        depre.save()

        # Load elem from database
        depre_db = Deprecation.objects.get(dep_datetime=depre.dep_datetime,
                                           cpeitem=depre.cpeitem)

        # Compare values
        assert depre.id == depre_db.id
        assert depre.dep_datetime == depre_db.dep_datetime
        assert depre.cpeitem == depre_db.cpeitem
