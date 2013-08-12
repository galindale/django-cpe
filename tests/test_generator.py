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

from django.utils import timezone
from django.core.exceptions import ValidationError
from model_mommy import mommy

from djangocpe.models import Generator, CpeList


@pytest.mark.django_db
class TestGenerator:
    """
    Tests to check operations with generator elements
    of CPE dictionary model.
    """

    def test_good_gen(self):
        """
        Check the creation of a correct generator element.
        """

        # Create CPE list element in database
        clist = mommy.make(CpeList)

        # Create and save generator elem in database
        schema_version = "2.2"
        timestamp = timezone.now()
        gen = Generator(schema_version=schema_version,
                        timestamp=timestamp,
                        cpelist=clist)

        gen.save()

        # Load elem from database
        gen_db = Generator.objects.get(schema_version=schema_version,
                                       timestamp=timestamp,
                                       cpelist=clist)

        assert gen.id == gen_db.id
