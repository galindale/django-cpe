#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is part of django-cpe package.

This module implements the importation of CPE Dictionaries version 2.3,
specified as XML files, in the models of package django-cpe.

Copyright (C) 2013  Alejandro Galindo Garcí Roberto Abdelkader Martíz Péz

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

- Alejandro Galindo Garcí galindo.garcia.alejandro@gmail.com
- Roberto Abdelkader Martíz Péz: robertomartinezp@gmail.com
"""

from iso8601 import iso8601
from xml.sax.handler import ContentHandler
from datetime import datetime

from cpe import CPE
from djangocpe.models import CpeList, Generator, CpeData, CpeItem, Title, Note
from django.db.utils import IntegrityError


class Cpedict23Handler(ContentHandler):
    """
    A handler to deal with CPE Dictionaries defined in XML format.
    """
    # ------- CPE-LIST ------

    TAG_CPELIST = "cpe-list"

    ATT_CPELIST_NAME = "name"

    # ------ GENERATOR ------

    TAG_GEN = "generator"

    TAG_PROD_NAME = "product_name"
    TAG_PROD_VER = "product_version"
    TAG_SCHEMA_VER = "schema_version"
    TAG_TIMESTAMP = "timestamp"

    # ------- CPE-ITEM -------

    TAG_CPEITEM = "cpe-item"
    ATT_CPEITEM_NAME = "name"

    # ------ CPE23-ITEM ------

    TAG_CPEITEM_23 = "cpe-23:cpe23-item"
    ATT_CPEITEM_23_NAME = "name"
    ATT_CPEITEM_23_DEPRECATED = "deprecated"
    ATT_CPEITEM_23_DEPDATE = "deprecation_date"

    # -------- TITLE ---------

    TAG_TITLE = "title"
    ATT_TITLE_LANG = "xml:lang"

    # --------- NOTE ---------

    TAG_NOTE_LIST = "notes"
    TAG_NOTE = "note"
    ATT_NOTE_LANG = "xml:lang"

    def __init__(self, *args, **kwargs):
        """
        Initialization of condition variables and objects to store input
        values.
        """

        # ------ CPE-LIST ------

        self.inCpelist = False
        self.cpelist = CpeList()

        # ------ GENERATOR ------

        self.inGenerator = False

        self.inGenProdName = False
        self.inGenProdVer = False
        self.inGenSchemaVer = False
        self.inGenTimestamp = False

        self.generator = Generator()

        # ------- CPE-ITEM ------

        self.inCpeitem = False
        self.cpeitem = dict()

        # ------ CPE23-ITEM -----

        self.cpeitem23 = dict()
        self.cpeitem23_db = None

        # -------- TITLE --------

        self.inTitle = False
        self.titles = []

        # -------- NOTE --------

        self.inNote = False
        self.inNotelist = False
        self.notes = []

    def _startCpeList(self, name, attributes):
        """
        Analyzes the input opening tag corresponds to a cpe-list element.

        :param string name: The opening tag name of element
        :param Atributes attributes: List of element attributes
        :returns: None
        """

        self.inCpelist = True

        # Store values of cpe list element

        timenow = iso8601.datetime.now().isoformat()
        self.cpelist.name = timenow
        self.cpelist.save()

    def _startGenerator(self, name, attributes):
        """
        Analyzes the input opening tag corresponds to a generator element.

        :param string name: The opening tag name of element
        :param Atributes attributes: List of element attributes
        :returns: None
        """

        self.inGenerator = True

        # Initializes the optional attributes of generator element
        self.generator.product_name = ""
        self.generator.product_version = ""

    def _startCpeItem(self, name, attributes):
        """
        Analyzes the input opening tag corresponds to a cpe-item element.

        :param string name: The opening tag name of element
        :param Atributes attributes: List of element attributes
        :returns: None
        """

        self.inCpeitem = True

        # This name corresponds to version 2.2 of CPE.
        # It is necessary to check valid name but not save in database
        name = attributes.get(self.ATT_CPEITEM_NAME)
        self.cpeitem[self.ATT_CPEITEM_NAME] = name

    def _startCpeItem23(self, name, attributes):
        """
        Analyzes the input opening tag corresponds to a cpe23-item element.

        :param string name: The opening tag name of element
        :param Atributes attributes: List of element attributes
        :returns: None
        """

        name = attributes.get(self.ATT_CPEITEM_23_NAME)
        self.cpeitem23[self.ATT_CPEITEM_23_NAME] = name

        deprecated = attributes.get(self.ATT_CPEITEM_23_DEPRECATED)
        if deprecated is None:
            deprecated = False
        self.cpeitem23[self.ATT_CPEITEM_23_DEPRECATED] = deprecated

        depdate = attributes.get(self.ATT_CPEITEM_23_DEPDATE)
        self.cpeitem23[self.ATT_CPEITEM_23_DEPDATE] = depdate

    def _startTitle(self, name, attributes):
        """
        Analyzes the input opening tag corresponds to a title element.

        :param string name: The opening tag name of element
        :param Atributes attributes: List of element attributes
        :returns: None
        """

        language = attributes.get(self.ATT_TITLE_LANG)
        title_values = Title()
        title_values.language = language

        self.titles.append(title_values)

        self.inTitle = True

    def _startNoteList(self, name, attributes):
        """
        Analyzes the input opening tag corresponds to a note element.

        :param string name: The opening tag name of element
        :param Atributes attributes: List of element attributes
        :returns: None
        """

        self.inNotelist = True

        language = attributes.get(self.ATT_NOTE_LANG)
        note_values = Note()
        note_values.language = language

        self.notes.append(note_values)

    def startElement(self, name, attributes):
        """
        Analyzes the input opening tag of an element.

        :param string name: The opening tag name of element
        :param Attributes attributes: List of element attributes
        :returns: None
        """
        # ------ CPE-LIST ------

        if name == self.TAG_CPELIST:
            self._startCpeList(name, attributes)

        elif self.inCpelist:

            # ------ GENERATOR ------

            if name == self.TAG_GEN:
                self._startGenerator(name, attributes)

            elif self.inGenerator:
                if name == self.TAG_PROD_NAME:
                    self.inGenProdName = True

                elif name == self.TAG_PROD_VER:
                    self.inGenProdVer = True

                elif name == self.TAG_SCHEMA_VER:
                    self.inGenSchemaVer = True

                elif name == self.TAG_TIMESTAMP:
                    self.inGenTimestamp = True

            # ------ CPE-ITEM ------

            elif name == self.TAG_CPEITEM:
                self._startCpeItem(name, attributes)

            elif self.inCpeitem:

                # ----- CPE23-ITEM -----

                if name == self.TAG_CPEITEM_23:
                    self._startCpeItem23(name, attributes)

                # -------- TITLE -------

                elif name == self.TAG_TITLE:
                    self._startTitle(name, attributes)

                # --------- NOTE -------

                elif name == self.TAG_NOTE_LIST:
                    self._startNoteList(name, attributes)

                elif self.inNotelist:

                    if name == self.TAG_NOTE:
                        self.inNote = True

    def characters(self, chars):
        """
        Analyzes the content of a XML element.

        :param string chars: The content of element as string
        :returns: None
        """
        # ------ GENERATOR ------
        if self.inGenerator:
            if self.inGenProdName:
                self.generator.product_name = chars
            if self.inGenProdVer:
                self.generator.product_version = chars
            if self.inGenSchemaVer:
                self.generator.schema_version = chars
            if self.inGenTimestamp:
                self.generator.timestamp = chars

        # -------- TITLE -------

        elif self.inTitle:
            # Set the title of last title element found
            self.titles[-1].title = chars

        # --------- NOTE -------

        elif self.inNote:
            # Set the note of last note element found
            self.notes[-1].note = chars

    def _endGenerator(self, name):
        """
        Analyzes the input ending tag corresponds to a generator element.

        :param string name: The ending tag name of an element
        :returns: None
        """

        self.inGenerator = False

        # Save the generator element

        self.generator.cpelist = self.cpelist
        self.generator.save()

    def _endCpeItem(self, name):
        """
        Analyzes the input ending tag corresponds to a cpe-item element.

        :param string name: The ending tag name of element
        :returns: None
        """

        self.inCpeitem = False

        # Check if CPE Name version 2.2 is valid
        cpe_str = self.cpeitem[self.ATT_CPEITEM_NAME]
        try:
            CPE(cpe_str, CPE.VERSION_2_2)
        except:
            # TODO: create parser exception
            raise
        else:
            # Check if CPE Name version 2.3 is valid
            cpe23_str = self.cpeitem23[self.ATT_CPEITEM_23_NAME]

            try:
                cpe23 = CPE(cpe23_str, CPE.VERSION_2_3)
            except:
                # TODO: create parser exception
                raise
            else:
                # Convert CPE Name version 2.3 in WFN style
                # because it is the default style in database

                cpe23_wfn = CPE(cpe23.as_wfn(), CPE.VERSION_2_3)

                part = cpe23_wfn.get_part()[0]
                vendor = cpe23_wfn.get_vendor()[0]
                product = cpe23_wfn.get_product()[0]
                version = cpe23_wfn.get_version()[0]
                update = cpe23_wfn.get_update()[0]
                edition = cpe23_wfn.get_edition()[0]
                sw_edition = cpe23_wfn.get_software_edition()[0]
                target_sw = cpe23_wfn.get_target_software()[0]
                target_hw = cpe23_wfn.get_target_hardware()[0]
                other = cpe23_wfn.get_other()[0]
                language = cpe23_wfn.get_language()[0]

                # Find out if cpedata exists already
                cpe_list = CpeData.objects.filter(part=part,
                                                  vendor=vendor,
                                                  product=product,
                                                  version=version,
                                                  update=update,
                                                  edition=edition,
                                                  sw_edition=sw_edition,
                                                  target_sw=target_sw,
                                                  target_hw=target_hw,
                                                  other=other,
                                                  language=language)
                if len(cpe_list) == 0:
                    # Save the new cpedata element

                    cpedata = CpeData(part=part,
                                      vendor=vendor,
                                      product=product,
                                      version=version,
                                      update=update,
                                      edition=edition,
                                      sw_edition=sw_edition,
                                      target_sw=target_sw,
                                      target_hw=target_hw,
                                      other=other,
                                      language=language)

                    cpedata.save()
                else:
                    # Get the cpedata stored in the database
                    cpedata = cpe_list[0]

                # Save the cpeitem element

                depre = self.cpeitem23[self.ATT_CPEITEM_23_DEPRECATED]
                depdate = self.cpeitem23[self.ATT_CPEITEM_23_DEPDATE]

                self.cpeitem23_db = CpeItem(deprecated=depre,
                                            deprecation_date=depdate,
                                            name=cpedata,
                                            cpelist=self.cpelist)
                self.cpeitem23_db.save()

                if len(self.titles) > 0:
                    # Title elements must be saved after cpe-item element
                    # because of the dependency between each other
                    for tit in self.titles:
                        tit.cpeitem = self.cpeitem23_db
                        tit.save()

                if len(self.notes) > 0:
                    # Note elements must be saved after cpe-item element
                    # because of the dependency between each other
                    for note in self.notes:
                        note.cpeitem = self.cpeitem23_db
                        note.save()

    def endElement(self, name):
        """
        Analyzes the input ending tag of an element.

        :param string name: The ending tag name
        :returns: None
        """

        # ------ CPE-LIST ------

        if name == self.TAG_CPELIST:
            self.inCpelist = False

        elif self.inCpelist:

            # ----- GENERATOR ------

            if name == self.TAG_GEN:
                self._endGenerator(name)

            elif self.inGenerator:

                if name == self.TAG_PROD_NAME:
                    self.inGenProdName = False

                elif name == self.TAG_PROD_VER:
                    self.inGenProdVer = False

                elif name == self.TAG_SCHEMA_VER:
                    self.inGenSchemaVer = False

                elif name == self.TAG_TIMESTAMP:
                    self.inGenTimestamp = False

            # ------ CPE-ITEM ------

            elif name == self.TAG_CPEITEM:
                self._endCpeItem(name)

            elif self.inCpeitem:

                # ------- TITLE --------

                if name == self.TAG_TITLE:
                    self.inTitle = False

                # -------- NOTE --------

                elif name == self.TAG_NOTE_LIST:
                    self.inNotelist = False

                elif self.inNotelist:

                    if name == self.TAG_NOTE:
                        self.inNote = False
