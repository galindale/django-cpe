# -*- coding: utf-8 -*-

"""
This file is part of django-cpe package.

This module contains the tests to check operations of cpe-item elements of
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

from djangocpe.models import CpeItem, CpeList
from .fixtures import good_cpedata


@pytest.mark.django_db
class TestCpeItem:
    """
    Tests to check operations with cpe-item elements
    of CPE dictionary model.
    """

    def test_good_cpeitem_min_fields(self, good_cpedata):
        """
        Check the creation of a correct cpe-item element
        with all fields filled.
        """

        # Create CPE list element in database
        clist = mommy.make(CpeList)

        # Create a cpe data element in database
        cpename = good_cpedata
        cpename.full_clean()
        cpename.save()

        # Create and save cpe item
        cpeitem = CpeItem(name=cpename,
                          cpelist=clist)

        cpeitem.save()

        # Load elem from database
        cpeitem_db = CpeItem.objects.get(
            name=cpeitem.name,
            deprecated=cpeitem.deprecated,
            deprecation_date=cpeitem.deprecation_date,
            deprecated_by=cpeitem.deprecated_by,
            cpelist=cpeitem.cpelist)

        assert cpeitem.id == cpeitem_db.id
        assert cpeitem.name == cpeitem_db.name
        assert cpeitem.deprecated == cpeitem_db.deprecated
        assert cpeitem.deprecation_date == cpeitem_db.deprecation_date
        assert cpeitem.deprecated_by == cpeitem_db.deprecated_by
        assert cpeitem.cpelist == cpeitem_db.cpelist

    def test_good_cpeitem_all_fields(self, good_cpedata):
        """
        Check the creation of a correct cpe-item element
        with all fields filled.
        """

        # Create CPE list element in database
        clist = mommy.make(CpeList)

        # Create two cpe data elements in database
        cpename = good_cpedata
        cpename.full_clean()
        cpename.save()

        cpedepre = good_cpedata
        cpedepre.part = '"h"'
        cpedepre.full_clean()
        cpedepre.save()

        # Create and save cpe item
        deprecated = False
        date = timezone.now()
        cpeitem = CpeItem(name=cpename,
                          deprecated=deprecated,
                          deprecation_date=date,
                          deprecated_by=cpedepre,
                          cpelist=clist)

        cpeitem.save()

        # Load elem from database
        cpeitem_db = CpeItem.objects.get(
            name=cpeitem.name,
            deprecated=cpeitem.deprecated,
            deprecation_date=cpeitem.deprecation_date,
            deprecated_by=cpeitem.deprecated_by,
            cpelist=cpeitem.cpelist)

        assert cpeitem.id == cpeitem_db.id
        assert cpeitem.name == cpeitem_db.name
        assert cpeitem.deprecated == cpeitem_db.deprecated
        assert cpeitem.deprecation_date == cpeitem_db.deprecation_date
        assert cpeitem.deprecated_by == cpeitem_db.deprecated_by
        assert cpeitem.cpelist == cpeitem_db.cpelist
