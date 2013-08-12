# -*- coding: utf-8 -*-

"""
This file is part of django-cpe package.

This module contains the tests to check operations of reference elements of
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

from django.core.exceptions import ValidationError
from model_mommy import mommy

from djangocpe.models import Reference, CpeItem


@pytest.mark.django_db
class TestReference:
    """
    Tests to check operations with reference elements
    of CPE dictionary model.
    """

    def test_good_reference(self):
        """
        Check the creation of a correct reference element.
        """

        # Create reference element in database
        cpeitem = mommy.make(CpeItem)
        ref = mommy.prepare(Reference,
                            url="http://www.mitre.org",
                            cpeitem=cpeitem)

        # Object validation
        ref.full_clean(['description'])
        ref.save()

        # Load elem from database
        ref_db = Reference.objects.get(name=ref.name,
                                       url=ref.url)

        assert ref.id == ref_db.id

    def test_bad_reference_uri(self):
        """
        Check the creation of a reference element with an invalid URI value.
        """

        ref = mommy.prepare(Reference, url="baduri")

        with pytest.raises(ValidationError) as e:
            ref.full_clean(['description'])

        assert 'url' in str(e.value)
