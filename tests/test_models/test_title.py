# -*- coding: utf-8 -*-

"""
This file is part of django-cpe package.

This module contains the tests to check operations of title elements of
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

from djangocpe.models import Title, CpeItem


@pytest.mark.django_db
class TestTitle:
    """
    Tests to check operations with title elements
    of CPE dictionary model.
    """

    def test_good_title_all_fields(self):
        """
        Check the creation of a correct title element
        with all fields filled.
        """

        # Create title element in database
        cpeitem = mommy.make(CpeItem)
        t = mommy.prepare(Title, language="es-ES", cpeitem=cpeitem)

        # Element validation
        t.full_clean()

        # Save element in database
        t.save()

        # Load elem from database
        title_db = Title.objects.get(title=t.title,
                                     language=t.language)

        assert t.id == title_db.id
        assert t.title == title_db.title
        assert t.language == title_db.language

    def test_bad_title_language(self):
        """
        Check the creation of a title element with an invalid language value.
        """

        t = mommy.prepare(Title, language="es**ES")

        with pytest.raises(ValidationError) as e:
            t.full_clean()

        assert 'language' in str(e.value)
