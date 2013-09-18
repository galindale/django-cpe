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

    def _check_title(self, xmlpath, title):
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
        title_list = Title.objects.filter(title=title.title,
                                          language=title.language)
        #title_db = title_list[0]
        print title_list
        print title

        # Check if test title element is stored in database
        #assert title_db.title == title.title
        #assert title_db.language == title.language

    def test_good_title_one(self):
        """
        Check the import of a title element.
        """

        # XML CPE Dictionary path
        XML_PATH = './xml/cpedict_v2.3_title_one.xml'

        # Generator values
        title = "1024cms.org 1024 CMS 1.4.1"
        language = "en-US"

        title_db = Title(title=title, language=language)

        # Check title element
        self._check_title(XML_PATH, title_db)

    def test_good_title_two(self):
        """
        Check the import of two title elements.
        """

        # XML CPE Dictionary path
        XML_PATH = './xml/cpedict_v2.3_title_two.xml'

        # Values of titles
        title1 = "Elemata CMS 3.0 release candidate"
        language1 = "en-US"
        title1_db = Title(title=title1, language=language1)

        title2 = u"Elemata CMS 3.0 versióandidata"
        language2 = "es-es"
        title2_db = Title(title=title2, language=language2)

        # Check first title element
        self._check_title(XML_PATH, title1_db)
        self._check_title(XML_PATH, title2_db)
