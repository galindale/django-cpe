# -*- coding: utf-8 -*-

"""
This file is part of django-cpe package.

This module contains the tests to check import operation with the parser
associated with generator elements in a CPE Dictionary version 2.3 as XML file.

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

from djangocpe.models import Generator
from decimal import Decimal

import function_parsing


@pytest.mark.django_db
class TestCpe23Generator:
    """
    Tests to check import operation with a generator element
    in CPE dictionary as XML file.
    """

    dirpath = "{0}{1}xml{2}".format(os.path.abspath("."), os.sep, os.sep)

    def _check_generator(self, gen):
        """
        Get the generator values and check if they are saved correctly
        in database.

        :param Generator gen: The values of generator element
        :returns: None
        """

        # Read generator element stored in database
        gen_list = Generator.objects.filter(product_name=gen.product_name,
                                            product_version=gen.product_version,
                                            schema_version=gen.schema_version,
                                            timestamp=gen.timestamp)

        gen_db = gen_list[0]

        # Check if test generator element is stored in database
        assert gen_db.product_name == gen.product_name
        assert gen_db.product_version == gen.product_version
        assert gen_db.schema_version == gen.schema_version

        # Convert datetime string in ISO 8601 datetime value
        isodate = iso8601.parse_date(gen.timestamp)

        assert gen_db.timestamp == isodate

    def test_good_gen_min_fields(self):
        """
        Check the import of a minimum generator element (only required fields).
        """

        # The XML filepath with the CPE Dictionary
        XML_PATH = "{0}cpedict_v2.3_generator_min_fields.xml".format(
            self.dirpath)

        # Parse input XML file
        function_parsing.parse_xmlfile(XML_PATH)

        # Generator values
        pn = ""
        pv = ""
        sv = Decimal("2.3")
        ts = "2013-09-05T03:50:00.193Z"
        iso8601.parse_date(ts)

        gen_db = Generator(product_name=pn, product_version=pv,
                           schema_version=sv, timestamp=ts)

        # Check generator element
        self._check_generator(gen_db)

    def test_good_gen_all_fields(self):
        """
        Check the import of a generator element with all fields filled.
        """

        # The XML filepath with the CPE Dictionary
        XML_PATH = "{0}cpedict_v2.3_generator_all_fields.xml".format(
            self.dirpath)

        # Parse input XML file
        function_parsing.parse_xmlfile(XML_PATH)

        # Generator values
        pn = "National Vulnerability Database (NVD)"
        pv = "2.20.0-SNAPSHOT (PRODUCTION)"
        sv = Decimal("2.3")
        ts = "2013-09-05T03:50:00.193Z"
        iso8601.parse_date(ts)

        gen_db = Generator(product_name=pn, product_version=pv,
                           schema_version=sv, timestamp=ts)

        # Check generator element
        self._check_generator(gen_db)
