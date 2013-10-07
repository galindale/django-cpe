# -*- coding: utf-8 -*-

"""
This file is part of django-cpe package.

This module contains the tests to check import operation with the parser
associated with submitter elements in a CPE Dictionary version 2.3
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

from djangocpe.models import Organization

import function_parsing


@pytest.mark.django_db
class TestCpe23Submitter:
    """
    Tests to check import operation with a submitter element
    in CPE dictionary as XML file.
    """

    dirpath = "{0}{1}xml{2}".format(os.path.abspath("."), os.sep, os.sep)

    def test_good_submitter_min_fields(self):
        """
        Check the import of a submitter element with only
        required fields filled.
        """

        # The XML filepath with the CPE Dictionary
        XML_PATH = "{0}cpedict_v2.3_submitter_min_fields.xml".format(
            self.dirpath)

        # Parse input XML file
        function_parsing.parse_xmlfile(XML_PATH)

        # Check submitter element
        system_id = "http://http://www.mitre.org/"
        name = "MITRE"

        # It is necessary to parse value
        # but the input type of datetime attribute must be a string
        dt_str = "2005-01-15T17:35:00.000-04:00"
        iso8601.parse_date(dt_str)
        action_datetime = dt_str

        submitter = Organization(system_id=system_id,
                                 name=name,
                                 action_datetime=dt,
                                 comment=comment)

        # Read element stored in database
        submitter_list = Organization.objects.filter(
            system_id=submitter.system_id,
            name=submitter.name,
            action_datetime=submitter.action_datetime)

        submitter_db = submitter_list[0]

        # Check if test submitter element is stored in database
        assert submitter_db.system_id == submitter.system_id
        assert submitter_db.name == submitter.name
        assert submitter_db.action_datetime == submitter.action_datetime
        assert submitter_db.comment == submitter.comment

    def test_good_submitter_all_fields(self):
        """
        Check the import of a submitter element with all field filled.
        """

        # The XML filepath with the CPE Dictionary
        XML_PATH = "{0}cpedict_v2.3_submitter_all_fields.xml".format(
            self.dirpath)

        # Parse input XML file
        function_parsing.parse_xmlfile(XML_PATH)

        # Check submitter element
        system_id = "http://http://www.mitre.org/"
        name = "MITRE"
        comment = "Organization acting as the submitter"

        # It is necessary to parse value
        # but the input type of datetime attribute must be a string
        dt_str = "2005-01-15T17:35:00.000-04:00"
        iso8601.parse_date(dt_str)
        action_datetime = dt_str

        submitter = Organization(system_id=system_id,
                                 name=name,
                                 action_datetime=dt,
                                 comment=comment)

        # Read element stored in database
        submitter_list = Organization.objects.filter(
            system_id=submitter.system_id,
            name=submitter.name,
            action_datetime=submitter.action_datetime,
            comment=submitter.comment)

        submitter_db = submitter_list[0]

        # Check if test submitter element is stored in database
        assert submitter_db.system_id == submitter.system_id
        assert submitter_db.name == submitter.name
        assert submitter_db.action_datetime == submitter.action_datetime
        assert submitter_db.comment == submitter.comment
