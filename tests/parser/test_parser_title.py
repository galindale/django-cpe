# -*- coding: utf-8 -*-

"""
This file is part of django-cpe package.

This module contains the tests to check import operation with the parser
associated with title elements in a CPE Dictionary version 2.3 as XML file.

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

from djangocpe.cpedict_parser import CpedictParser
from djangocpe.cpedict23_handler import Cpedict23Handler
from djangocpe.models import Title

from cpe.cpe import CPE

@pytest.mark.django_db
class TestCpe23iTitle:
    """
    Tests to check import operation with a title element
    in CPE dictionary as XML file.
    """

    def _check_title(self, xmlpath, title, language):
        """
        Get the title values and check if they are saved correctly
        in database.
        """

        # Set handler
        handler = Cpedict23Handler()
        p = CpedictParser(handler)

        # Execute parser with input XML file
        p.parse(xmlpath)

        # Read title element stored in database
        title_db = Title.objects.get(title=title, language=language)

        # Check if test title element is stored in database
        assert title_db.title == title
        assert title_db.language == language

    def test_good_title_one(self):
        """
        Check the import of a title element.
        """

        # XML CPE Dictionary path
        XML_PATH = './xml/cpedict_v2.3_title_one.xml'

        # Generator values
        title = "1024cms.org 1024 CMS 1.4.1"
        language = "en-US"

        # Check title element
        self._check_title(XML_PATH, title, language)

#    def test_good_gen_all_fields(self):
#        """
#        Check the import of a generator element with all fields filled.
#        """
#
#        # XML CPE Dictionary path
#        XML_PATH = './xml/cpedict_v2.3_generator_all_fields.xml'
#
#        # Generator values
#        pn = "National Vulnerability Database (NVD)"
#        pv = "2.20.0-SNAPSHOT (PRODUCTION)"
#        sv = 2.3
#        ts = iso8601.parse_date("2013-09-05T03:50:00.193Z")
#
#        # Check generator element
#        self._check_generator(XML_PATH, pn, pv, sv, ts)
