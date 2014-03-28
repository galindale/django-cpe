# -*- coding: utf-8 -*-

"""
This file is part of django-cpe package.

This module contains the tests to check operations of generator elements of
CPE dictionary model.

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

from model_mommy import mommy

from djangocpe.models import Generator


@pytest.mark.django_db
class TestGenerator:
    """
    Tests to check operations with generator elements
    of CPE dictionary model.
    """

    def test_good_gen_min_fields(self):
        """
        Check the creation of a correct generator element
        with only required fields filled.
        """

        # Create and save generator elem in database
        gen = mommy.make(Generator)

        # Load elem from database
        gen_db = Generator.objects.get(product_name=gen.product_name,
                                       product_version=gen.product_version,
                                       schema_version=gen.schema_version,
                                       timestamp=gen.timestamp,
                                       cpelist=gen.cpelist)

        assert gen.id == gen_db.id
        assert gen.product_name == gen_db.product_name
        assert gen.product_version == gen_db.product_version
        assert gen.schema_version == gen_db.schema_version
        assert gen.timestamp == gen.timestamp
        assert gen.cpelist == gen.cpelist

    def test_good_gen_all_fields(self):
        """
        Check the creation of a correct generator element
        with all fields filled.
        """

        # Create and save generator elem in database
        gen = mommy.make(Generator,
                         product_name="National Vulnerability Database (NVD)",
                         product_version="2.20.0-SNAPSHOT (PRODUCTION)")

        # Load elem from database
        gen_db = Generator.objects.get(product_name=gen.product_name,
                                       product_version=gen.product_version,
                                       schema_version=gen.schema_version,
                                       timestamp=gen.timestamp,
                                       cpelist=gen.cpelist)

        assert gen.id == gen_db.id
        assert gen.product_name == gen_db.product_name
        assert gen.product_version == gen_db.product_version
        assert gen.schema_version == gen_db.schema_version
        assert gen.timestamp == gen.timestamp
        assert gen.cpelist == gen.cpelist
