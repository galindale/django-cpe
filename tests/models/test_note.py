# -*- coding: utf-8 -*-

"""
This file is part of django-cpe package.

This module contains the tests to check operations of note elements of
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

from djangocpe.models import Note, CpeItem


@pytest.mark.django_db
class TestNote:
    """
    Tests to check operations with note elements
    of CPE dictionary model.
    """

    def test_good_note(self):
        """
        Check the creation of a correct note element.
        """

        # Create note element in database
        cpeitem = mommy.make(CpeItem)
        n = mommy.prepare(Note, language="es-es", cpeitem=cpeitem)

        # Object validation
        n.full_clean(['description'])
        n.save()

        # Load elem from database
        note_db = Note.objects.get(note=n.note,
                                   language=n.language)

        assert n.id == note_db.id

    def test_bad_note_language(self):
        """
        Check the creation of a note element with an invalid language value.
        """

        n = mommy.prepare(Note, language="es**ES")

        with pytest.raises(ValidationError) as e:
            n.full_clean(['description'])

        assert 'language' in str(e.value)
