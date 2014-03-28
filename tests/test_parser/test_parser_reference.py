# -*- coding: utf-8 -*-

"""
This file is part of django-cpe package.

This module contains the tests to check import operation with the parser
associated with reference elements in a CPE Dictionary version 2.3 as XML file.

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

from djangocpe.models import Reference

import function_parsing


@pytest.mark.django_db
class TestCpe23Reference:
    """
    Tests to check import operation with a reference element
    in CPE dictionary as XML file.
    """

    dirpath = "{0}{1}xml{2}".format(os.path.abspath("."), os.sep, os.sep)

    def _check_reference(self, ref):
        """
        Get the reference values and check if they are saved correctly
        in database.

        :param Reference ref: The values of reference element
        :returns: None
        """

        # Read reference element stored in database
        reference_list = Reference.objects.filter(name=ref.name, href=ref.href)
        reference_db = reference_list[0]

        # Check if test reference element is stored in database
        assert reference_db.name == ref.name
        assert reference_db.href == ref.href

    def test_good_reference_one(self):
        """
        Check the import of a reference element.
        """

        # The XML filepath with the CPE Dictionary
        XML_PATH = "{0}cpedict_v2.3_reference_one.xml".format(self.dirpath)

        # Parse input XML file
        function_parsing.parse_xmlfile(XML_PATH)

        # Generator values
        name = "Version information"
        href = "http://www.emc.com/support/rsa/eops/agents.htm"

        reference_db = Reference(name=name, href=href)

        # Check reference element
        self._check_reference(reference_db)

    def test_good_reference_two(self):
        """
        Check the import of two reference elements.
        """

        # The XML filepath with the CPE Dictionary
        XML_PATH = "{0}cpedict_v2.3_reference_two.xml".format(self.dirpath)

        # Parse input XML file
        function_parsing.parse_xmlfile(XML_PATH)

        # Check first reference element
        name1 = "Version information"
        href1 = "http://www.emc.com/support/rsa/eops/agents.htm"
        reference1_db = Reference(name=name1, href=href1)

        self._check_reference(reference1_db)

        # Check second reference element
        name2 = "Authentication information"
        href2 = "http://www.emc.com/support/rsa/eops/adaptive-authentication.htm"
        reference2_db = Reference(name=name2, href=href2)

        self._check_reference(reference2_db)
