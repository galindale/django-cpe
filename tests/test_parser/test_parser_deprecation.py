# -*- coding: utf-8 -*-

"""
This file is part of django-cpe package.

This module contains the tests to check import operation with the parser
associated with deprecation elements in a CPE Dictionary version 2.3
as XML file.

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

from djangocpe.models import Deprecation

import function_parsing


@pytest.mark.django_db
class TestCpe23Deprecation:
    """
    Tests to check import operation with a deprecation element
    in CPE dictionary as XML file.
    """

    dirpath = "{0}{1}xml{2}".format(os.path.abspath("."), os.sep, os.sep)

    def _check_deprecation(self, depre):
        """
        Get the deprecation values and check if they are saved correctly
        in database.

        :param Deprecation deprecation: The values of deprecation element
        :returns: None
        """

        # Read deprecation element stored in database
        deprecation_list = Deprecation.objects.filter(
            dep_datetime=depre.dep_datetime)
        deprecation_db = deprecation_list[0]

        # Check if test deprecation element is stored in database
        if depre.dep_datetime is None:
            assert deprecation_db.dep_datetime == depre.dep_datetime
        else:
            # Convert datetime string in ISO 8601 datetime value
            isodate = iso8601.parse_date(depre.dep_datetime)

            assert deprecation_db.dep_datetime == isodate

    def test_good_deprecation_one(self):
        """
        Check the import of a deprecation element.
        """

        # The XML filepath with the CPE Dictionary
        XML_PATH = "{0}cpedict_v2.3_deprecation_one.xml".format(self.dirpath)

        # Parse input XML file
        function_parsing.parse_xmlfile(XML_PATH)

        # Deprecation values. It is necessary to parse value
        # but the input type of datetime attribute must be a string
        dt_str = "2008-04-15T12:35:00.000-04:00"
        iso8601.parse_date(dt_str)

        deprecation_db = Deprecation(dep_datetime=dt_str)

        # Check cpe-item element
        self._check_deprecation(deprecation_db)

    def test_good_deprecation_two(self):
        """
        Check the import of two deprecation elements.
        """

        # The XML filepath with the CPE Dictionary
        XML_PATH = "{0}cpedict_v2.3_deprecation_two.xml".format(self.dirpath)

        # Parse input XML file
        function_parsing.parse_xmlfile(XML_PATH)

        # Check first deprecation element
        depdate1 = None
        deprecation_db1 = Deprecation(dep_datetime=depdate1)

        self._check_deprecation(deprecation_db1)

        # Check second deprecation element
        # It is necessary to parse value
        # but the input type of datetime attribute must be a string
        dt_str = "2009-05-15T12:35:00.000-04:00"
        depdate2 = iso8601.parse_date(dt_str)

        deprecation_db2 = Deprecation(dep_datetime=dt_str)

        self._check_deprecation(deprecation_db2)
