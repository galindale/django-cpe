# -*- coding: utf-8 *-*

"""
This file is part of django-cpe package.

This module contains the tests to check operations of cpe-list elements of
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

from djangocpe.models import CpeList
from model_mommy import mommy
from .fixtures import good_cpedata


@pytest.mark.django_db
class TestCpeList:
    """
    Tests to check operations with cpe-list elements
    of CPE dictionary model.
    """

    def test_good_cpelist_min_fields(self, good_cpedata):
        """
        Check the creation of a correct cpe-list element
        with only required fields filled.
        """

        # Save elem in database
        clist = mommy.prepare(CpeList)
        clist.save()

        # Load elem from database
        clist_db = CpeList.objects.get(name=clist.name)

        assert clist.id == clist_db.id
        assert clist.name == clist_db.name

    def test_good_cpelist_all_fields(self, good_cpedata):
        """
        Check the creation of a correct cpe-list element
        with all fields filled.
        """

        # Save elem in database
        clist = mommy.prepare(CpeList, name="Clist name")
        clist.save()

        # Load elem from database
        clist_db = CpeList.objects.get(name=clist.name)

        assert clist.id == clist_db.id
        assert clist.name == clist_db.name
