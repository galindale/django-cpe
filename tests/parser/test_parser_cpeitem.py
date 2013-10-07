# -*- coding: utf-8 -*-

"""
This file is part of django-cpe package.

This module contains the tests to check import operation with the parser
associated with cpe-item elements in a CPE Dictionary version 2.3 as XML file.

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
import os

from iso8601 import iso8601

from djangocpe.models import CpeItem

import function_parsing


@pytest.mark.django_db
class TestCpe23CpeItem:
    """
    Tests to check import operation with a cpe-item element
    in CPE dictionary as XML file.
    """

    dirpath = "{0}{1}xml{2}".format(os.path.abspath("."), os.sep, os.sep)

    def _check_cpeitem(self, cpeitem):
        """
        Get the cpe-item values and check if they are saved correctly
        in database.

        :param CpeItem cpeitem: The values of cpe-item element
        :returns: None
        """

        # Read cpe-item element stored in database
        cpeitem_list = CpeItem.objects.filter(
            deprecated=cpeitem.deprecated,
            deprecation_date=cpeitem.deprecation_date)

        cpeitem_db = cpeitem_list[0]

        # Check if test cpe-item element is stored in database
        assert cpeitem_db.deprecated == cpeitem.deprecated

        if cpeitem.deprecation_date is None:
            assert cpeitem_db.deprecation_date == cpeitem.deprecation_date
        else:
            # Convert datetime string in ISO 8601 datetime value
            isodate = iso8601.parse_date(cpeitem.deprecation_date)

            assert cpeitem_db.deprecation_date == isodate

    def test_good_cpeitem_min_fields(self):
        """
        Check the import of a minimum cpe-item element (only required fields).
        """

        # The XML filepath with the CPE Dictionary
        XML_PATH = "{0}cpedict_v2.3_cpeitem_min_fields.xml".format(
            self.dirpath)

        # Parse input XML file
        function_parsing.parse_xmlfile(XML_PATH)

        # Cpe-item values
        deprecated = False
        depdate = None

        cpeitem_db = CpeItem(deprecated=deprecated, deprecation_date=depdate)

        # Check cpe-item element
        self._check_cpeitem(cpeitem_db)

    def test_good_cpeitem_all_fields(self):
        """
        Check the import of a cpe-item element with all fields filled.
        """

        # The XML filepath with the CPE Dictionary
        XML_PATH = "{0}cpedict_v2.3_cpeitem_all_fields.xml".format(
            self.dirpath)

        # Parse input XML file
        function_parsing.parse_xmlfile(XML_PATH)

        # Generator values
        deprecated = True
        depdate = "2010-12-28T17:36:01.163Z"

        # Check valid datetime value
        iso8601.parse_date(depdate)

        cpeitem_db = CpeItem(deprecated=deprecated, deprecation_date=depdate)

        # Check cpe-item element
        self._check_cpeitem(cpeitem_db)
