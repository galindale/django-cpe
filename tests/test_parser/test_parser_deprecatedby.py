# -*- coding: utf-8 -*-

"""
This file is part of django-cpe package.

This module contains the tests to check import operation with the parser
associated with deprecated-by elements in a CPE Dictionary version 2.3
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

from djangocpe.models import DeprecatedBy
from djangocpe.models import DEPRECATED_BY_NAME_CORRECTION
from djangocpe.models import DEPRECATED_BY_NAME_REMOVAL
from djangocpe.models import DEPRECATED_BY_ADDITIONAL_INFO

import function_parsing


@pytest.mark.django_db
class TestCpe23DeprecatedBy:
    """
    Tests to check import operation with a deprecated-by element
    in CPE dictionary as XML file.
    """

    dirpath = "{0}{1}xml{2}".format(os.path.abspath("."), os.sep, os.sep)

    def test_good_deprecatedby_two(self):
        """
        Check the import of two deprecated-by elements.
        """

        # The XML filepath with the CPE Dictionary
        XML_PATH = "{0}cpedict_v2.3_deprecatedby.xml".format(self.dirpath)

        # Parse input XML file
        function_parsing.parse_xmlfile(XML_PATH)

        # Check first deprecated-by element
        deptype1 = DEPRECATED_BY_NAME_CORRECTION
        depby1 = DeprecatedBy(dep_type=deptype1)

        # Read deprecated-by element stored in database
        deprecatedby_list = DeprecatedBy.objects.filter(
            dep_type=depby1.dep_type)

        deprecatedby_db1 = deprecatedby_list[0]

        # Check if test deprecated-by element is stored in database
        assert deprecatedby_db1.dep_type == depby1.dep_type

        # Check second deprecated-by element
        deptype2 = DEPRECATED_BY_NAME_REMOVAL
        depby2 = DeprecatedBy(dep_type=deptype2)

        # Read deprecated-by element stored in database
        deprecatedby_list = DeprecatedBy.objects.filter(
            dep_type=depby2.dep_type)

        deprecatedby_db2 = deprecatedby_list[0]

        # Check if test deprecated-by element is stored in database
        assert deprecatedby_db2.dep_type == depby2.dep_type

        # Check third deprecated-by element
        deptype3 = DEPRECATED_BY_ADDITIONAL_INFO
        depby3 = DeprecatedBy(dep_type=deptype3)

        # Read deprecated-by element stored in database
        deprecatedby_list = DeprecatedBy.objects.filter(
            dep_type=depby3.dep_type)

        deprecatedby_db3 = deprecatedby_list[0]

        # Check if test deprecated-by element is stored in database
        assert deprecatedby_db3.dep_type == depby3.dep_type
