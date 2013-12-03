# -*- coding: utf-8 -*-

"""
This file is part of django-cpe package.

This module contains the tests to check import operation with the parser
associated with change description elements in a CPE Dictionary version 2.3
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

from djangocpe.models import ChangeDescription
from djangocpe.models import CHANGE_DEPRECATION
from djangocpe.models import CHANGE_ORIGINAL_RECORD
from djangocpe.models import CHANGE_AUTHORITY_CHANGE

import function_parsing


@pytest.mark.django_db
class TestCpe23ChangeDescription:
    """
    Tests to check import operation with a change description element
    in CPE dictionary as XML file.
    """

    dirpath = "{0}{1}xml{2}".format(os.path.abspath("."), os.sep, os.sep)

    def test_good_changedescription_one(self):
        """
        Check the import of one change description element.
        """

        # The XML filepath with the CPE Dictionary
        XML_PATH = "{0}cpedict_v2.3_changedescription_one.xml".format(
            self.dirpath)

        # Parse input XML file
        function_parsing.parse_xmlfile(XML_PATH)

        # Check first element
        ctype = CHANGE_DEPRECATION
        cdt = "2012-08-11T09:20:00.000-04:00"

        # Check the style ISO 8601 of input datetime value
        iso8601.parse_date(cdt)

        changedesc = ChangeDescription(change_type=ctype,
                                       change_datetime=cdt)

        # Read first element stored in database
        changedesc_list = ChangeDescription.objects.filter(
            change_type=changedesc.change_type,
            change_datetime=changedesc.change_datetime)

        changedesc_db = changedesc_list[0]

        # Check if first element is stored in database
        assert changedesc_db.change_type == changedesc.change_type

        isodate = iso8601.parse_date(changedesc.change_datetime)
        assert changedesc_db.change_datetime == isodate

    def test_good_changedescription_two(self):
        """
        Check the import of two change description elements.
        """

        # The XML filepath with the CPE Dictionary
        XML_PATH = "{0}cpedict_v2.3_changedescription_two.xml".format(
            self.dirpath)

        # Parse input XML file
        function_parsing.parse_xmlfile(XML_PATH)

        # Check first element
        ctype1 = CHANGE_ORIGINAL_RECORD
        cdt1 = "2008-03-15T12:35:00.000-04:00"
        comment1 = "The curator of the dictionary discovered information that led to a change."

        # Check the style ISO 8601 of input datetime value
        iso8601.parse_date(cdt1)

        changedesc1 = ChangeDescription(change_type=ctype1,
                                        change_datetime=cdt1,
                                        comment=comment1)

        # Read first element stored in database
        changedesc1_list = ChangeDescription.objects.filter(
            change_type=changedesc1.change_type,
            change_datetime=changedesc1.change_datetime,
            comment=changedesc1.comment)

        print ChangeDescription.objects.all()
        a = ChangeDescription.objects.all()[0]
        print "\n----------"
        print a.change_type
        print a.change_datetime
        print a.comment
        b = ChangeDescription.objects.all()[1]
        print "\n----------"
        print b.change_type
        print b.change_datetime
        print b.comment

        #changedesc_db1 = changedesc1_list[0]

        # Check if first element is stored in database
        #assert changedesc_db1.change_type == changedesc1.change_type
        #assert changedesc_db1.change_datetime == changedesc1.change_datetime

#        # Check second element
#        ctype2 = CHANGE_AUTHORITY_CHANGE
#        cdt2 = "2008-04-03T12:35:00.000-04:00"
#
#        # Check the style ISO 8601 of input datetime value
#        iso8601.parse_date(cdt2)
#
#        changedesc2 = ChangeDescription(change_type=ctype2,
#                                        change_datetime=cdt2)
#
#        # Read element stored in database
#        changedesc2_list = ChangeDescription.objects.filter(
#            change_type=changedesc2.change_type,
#            change_datetime=changedesc2.change_datetime)
#
#        changedesc_db2 = changedesc2_list[0]
#
#        # Check if test element is stored in database
#        assert changedesc_db2.change_type == changedesc2.change_type
#        assert changedesc_db2.change_datetime == changedesc2.change_datetime
