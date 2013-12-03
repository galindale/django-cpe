# -*- coding: utf-8 -*-

"""
This file is part of django-cpe package.

This module contains the tests to check import operation with the parser
associated with check elements in a CPE Dictionary version 2.3 as XML file.

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

from djangocpe.models import Check

from cpe.cpe import CPE

import function_parsing


@pytest.mark.django_db
class TestCpe23Check:
    """
    Tests to check import operation with a check element
    in CPE dictionary as XML file.
    """

    dirpath = "{0}{1}xml{2}".format(os.path.abspath("."), os.sep, os.sep)

    def _check_check(self, check):
        """
        Get the check values and check if they are saved correctly
        in database.
        
        :param Check check: The values of check element
        :returns: None
        """

        # Read check element stored in database
        check_list = Check.objects.filter(check_id=check.check_id,
                                          href=check.href,
                                          system=check.system)
        check_db = check_list[0]

        # Check if test check element is stored in database
        assert check_db.check_id == check.check_id
        assert check_db.href == check.href
        assert check_db.system == check.system

    def test_good_check_one(self):
        """
        Check the import of a check element.
        """

        # The XML filepath with the CPE Dictionary
        XML_PATH = "{0}cpedict_v2.3_check_one.xml".format(self.dirpath)

        # Parse input XML file
        function_parsing.parse_xmlfile(XML_PATH)

        # Generator values
        check_id = "oval:org.mitre.oval:def:310"
        href = "http://oval.mitre.org/repository/data/DownloadDefinition?id=oval:org.mitre.oval:def:310"
        system = "http://oval.mitre.org/XMLSchema/oval-definitions-5"

        check_db = Check(check_id=check_id, href=href, system=system)

        # Check check element
        self._check_check(check_db)

    def test_good_check_two(self):
        """
        Check the import of two check elements.
        """

        # The XML filepath with the CPE Dictionary
        XML_PATH = "{0}cpedict_v2.3_check_two.xml".format(self.dirpath)

        # Parse input XML file
        function_parsing.parse_xmlfile(XML_PATH)

        # Check first check element
        check_id1 = "oval:org.mitre.oval:def:310"
        href1 = "http://oval.mitre.org/repository/data/DownloadDefinition?id=oval:org.mitre.oval:def:310"
        system1 = "http://oval.mitre.org/XMLSchema/oval-definitions-5"

        check_db1 = Check(check_id=check_id1, href=href1, system=system1)

        # Check check element
        self._check_check(check_db1)

        # Check second check element
        check_id2 = "oval:org.mitre.oval:def:1937"
        href2 = None
        system2 = "http://oval.mitre.org/XMLSchema/oval-definitions-3"

        check_db2 = Check(check_id=check_id2, href=href2, system=system2)

        # Check check element
        self._check_check(check_db2)
