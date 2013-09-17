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

from iso8601 import iso8601

from djangocpe.cpedict_parser import CpedictParser
from djangocpe.cpedict23_handler import Cpedict23Handler
from djangocpe.models import Generator


@pytest.mark.django_db
class TestCpe23Generator:
    """
    Tests to check import operation with a generator element
    in CPE dictionary as XML file.
    """

    def _check_generator(self, xmlpath,
                         prodname, prodver, schemaver, timestamp):
        """
        Get the generator values and check if they are saved correctly
        in database.
        """

        # Search generator elements in database and save their IDs
        gen_list_prev = Generator.objects.filter(product_name=prodname,
                                                 product_version=prodver,
                                                 schema_version=schemaver,
                                                 timestamp=timestamp)
        id_list_prev = gen_list_prev.values_list('id')

        gen_ids_prev = []
        for id in id_list_prev:
            gen_ids_prev.append(id[0])

        # Set handler
        handler = Cpedict23Handler()
        p = CpedictParser(handler)

        # Execute parser with input XML file
        p.parse(xmlpath)

        # Read generator element stored in database
        gen_list_post = Generator.objects.filter(product_name=prodname,
                                                 product_version=prodver,
                                                 schema_version=schemaver,
                                                 timestamp=timestamp)

        id_list_post = gen_list_post.values_list('id')

        gen_ids_post = []
        for id in id_list_post:
            gen_ids_post.append(id[0])

        # Check if test generator element is stored in database
        assert len(gen_ids_post) == (len(gen_ids_prev) + 1)

    def test_good_gen_min_fields(self):
        """
        Check the import of a minimum generator element (only required fields).
        """

        # XML CPE Dictionary path
        XML_PATH = './xml/cpedict_v2.3_generator_min_fields.xml'

        # Generator values
        pn = ""
        pv = ""
        sv = 2.3
        ts = iso8601.parse_date("2013-09-05T03:50:00.193Z")

        # Check generator element
        self._check_generator(XML_PATH, pn, pv, sv, ts)

    def test_good_gen_all_fields(self):
        """
        Check the import of a generator element with all fields filled.
        """

        # XML CPE Dictionary path
        XML_PATH = './xml/cpedict_v2.3_generator_all_fields.xml'

        # Generator values
        pn = "National Vulnerability Database (NVD)"
        pv = "2.20.0-SNAPSHOT (PRODUCTION)"
        sv = 2.3
        ts = iso8601.parse_date("2013-09-05T03:50:00.193Z")

        # Check generator element
        self._check_generator(XML_PATH, pn, pv, sv, ts)
