# -*- coding: utf-8 -*-

"""
This file is part of django-cpe package.

This module contains the tests to check import operation with the parser
associated with note elements in a CPE Dictionary version 2.3 as XML file.

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
from djangocpe.models import Note

from cpe.cpe import CPE


@pytest.mark.django_db
class TestCpe23Note:
    """
    Tests to check import operation with a note element
    in CPE dictionary as XML file.
    """

    def _check_note(self, xmlpath, note):
        """
        Get the note values and check if they are saved correctly
        in database.
        """

        # Set handler
        handler = Cpedict23Handler()
        p = CpedictParser(handler)

        # Execute parser with input XML file
        p.parse(xmlpath)

        # Read note element stored in database
        note_list = Note.objects.filter(language=note.language)
        note_db = note_list[0]

        # Check if test note element is stored in database
        assert note_db.note == note.note
        assert note_db.language == note.language

    def test_good_note_one(self):
        """
        Check the import of a note element.
        """

        # XML CPE Dictionary path
        XML_PATH = './xml/cpedict_v2.3_note_one.xml'

        # Generator values
        note = "Use product number and detail plain name"
        language = "en-US"

        note_db = Note(note=note, language=language)

        # Check note element
        self._check_note(XML_PATH, note_db)

    def test_good_note_two(self):
        """
        Check the import of two note elements.
        """

        # XML CPE Dictionary path
        XML_PATH = './xml/cpedict_v2.3_note_two.xml'

        # Check first note element
        note1 = "Use product number and detail plain name"
        language1 = "en-US"
        note1_db = Note(note=note1, language=language1)

        self._check_note(XML_PATH, note1_db)

        # Check second note element
        note2 = u"Usa el numero de producto y el nombre detallado"
        language2 = "es-ES"
        note2_db = Note(note=note2, language=language2)

        self._check_note(XML_PATH, note2_db)
