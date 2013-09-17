# -*- coding: utf-8 -*-

"""
This file is part of django-cpe package.

This module contains the tests to check import operation with the parser
associated with cpeitem elements in a CPE Dictionary version 2.3 as XML file.

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

from iso8601 import iso8601

from djangocpe.cpedict_parser import CpedictParser
from djangocpe.cpedict23_handler import Cpedict23Handler
from djangocpe.models import CpeItem


@pytest.mark.django_db
class TestCpe23CpeItem:
    """
    Tests to check import operation with a cpeitem element
    in CPE dictionary as XML file.
    """

    def _check_cpeitem(self, xmlpath, deprecated, depdate):
        """
        Get the cpeitem values and check if they are saved correctly
        in database.
        """

        # Search cpeitem elements in database and save their IDs
        cpeitem_list_prev = CpeItem.objects.filter(deprecated=deprecated,
                                                   deprecation_date=depdate)
        id_list_prev = cpeitem_list_prev.values_list('id')

        cpeitem_ids_prev = []
        for id in id_list_prev:
            cpeitem_ids_prev.append(id[0])

        # Set handler
        handler = Cpedict23Handler()
        p = CpedictParser(handler)

        # Execute parser with input XML file
        p.parse(xmlpath)

        # Read cpeitem element stored in database
        cpeitem_list_post = CpeItem.objects.filter(deprecated=deprecated,
                                                   deprecation_date=depdate)
        id_list_post = cpeitem_list_post.values_list('id')

        cpeitem_ids_post = []
        for id in id_list_post:
            cpeitem_ids_post.append(id[0])

        # Check if test cpeitem element is stored in database
        assert len(cpeitem_ids_post) == (len(cpeitem_ids_prev) + 1)

    def test_good_cpeitem_min_fields(self):
        """
        Check the import of a minimum cpeitem element (only required fields).
        """

        # XML CPE Dictionary path
        XML_PATH = './xml/cpedict_v2.3_cpeitem_min_fields.xml'

        # CpeItem values
        deprecated = False
        depdate = None

        # Check cpeitem element
        self._check_cpeitem(XML_PATH, deprecated, depdate)

    def test_good_cpeitem_all_fields(self):
        """
        Check the import of a cpeitem element with all fields filled.
        """

        # XML CPE Dictionary path
        XML_PATH = './xml/cpedict_v2.3_cpeitem_all_fields.xml'

        # Generator values
        deprecated = True
        depdate = iso8601.parse_date("2010-12-28T17:36:01.163Z")

        # Check generator element
        self._check_cpeitem(XML_PATH, deprecated, depdate)
