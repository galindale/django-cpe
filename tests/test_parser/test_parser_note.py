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
import os

from djangocpe.models import Note

import function_parsing


@pytest.mark.django_db
class TestCpe23Note:
    """
    Tests to check import operation with a note element
    in CPE dictionary as XML file.
    """

    dirpath = "{0}{1}xml{2}".format(os.path.abspath("."), os.sep, os.sep)

    def _check_note(self, notes):
        """
        Get the note values and check if they are saved correctly
        in database.

        :param Note note: The values of note element
        :returns: None
        """

        for n in notes:

            # Read note element stored in database
            note_list = Note.objects.filter(note=n.note, language=n.language)
            note_db = note_list[0]

            # Check if test note element is stored in database
            assert note_db.note == n.note
            assert note_db.language == n.language

    def test_good_notes_one(self):
        """
        Check the import of a notes element.
        """

        # The XML filepath with the CPE Dictionary
        XML_PATH = "{0}cpedict_v2.3_notes_one.xml".format(self.dirpath)

        # Parse input XML file
        function_parsing.parse_xmlfile(XML_PATH)

        noteList = []

        # Generator values
        note = "Use product number and detail plain name"
        language = "en-US"

        note_db = Note(note=note, language=language)
        noteList.append(note_db)

        # Check note element
        self._check_note(noteList)

    def test_good_notes_two(self):
        """
        Check the import of two notes elements.
        """

        # The XML filepath with the CPE Dictionary
        XML_PATH = "{0}cpedict_v2.3_notes_two.xml".format(self.dirpath)

        # Parse input XML file
        function_parsing.parse_xmlfile(XML_PATH)

        noteList = []

        # First note element
        note1 = "Use product number and detail plain name"
        language1 = "en-US"
        note1_db = Note(note=note1, language=language1)

        noteList.append(note1_db)

        # Second note element
        note2 = u"Usa el numero de producto y el nombre detallado"
        language2 = "es-ES"
        note2_db = Note(note=note2, language=language2)

        noteList.append(note2_db)

        # Check note element
        self._check_note(noteList)

    def test_good_notes_one_two(self):
        """
        Check the import of one notes element with two note subelements.
        """

        # The XML filepath with the CPE Dictionary
        XML_PATH = "{0}cpedict_v2.3_notes_one_two.xml".format(self.dirpath)

        # Parse input XML file
        function_parsing.parse_xmlfile(XML_PATH)

        language = "en-US"
        noteList = []

        # Check first note element
        note1 = "Use product number and detail plain name"
        note1_db = Note(note=note1, language=language)

        noteList.append(note1_db)

        # Check second note element
        note2 = "Another note about cpe name"
        note2_db = Note(note=note2, language=language)

        noteList.append(note2_db)

        self._check_note(noteList)
