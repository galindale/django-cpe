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
from djangocpe.models import CpeList, Generator, CpeData, CpeItem, Title
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

    def __init__(self, *args, **kwargs):
        """
        Initialization of condition variables and objects to store input
        values.
        """

        # ------ CPE-LIST ------

        self.inCpelist = False
        self.cpelist = dict()
        self.cpelist_db = None

        # ------ GENERATOR ------

        self.inGenerator = False

        self.inGenProdName = False
        self.inGenProdVer = False
        self.inGenSchemaVer = False
        self.inGenTimestamp = False

        self.generator = dict()

        # ------- CPE-ITEM ------

        self.inCpeitem = False
        self.cpeitem = dict()
        self.cpeitem_db = None

        # ------ CPE23-ITEM -----

        self.cpeitem23 = dict()

        # -------- TITLE --------

        self.inTitle = False
        self.title = dict()

    def _startCpeList(self, name, attributes):
        """
        Returns True if the input opening tag corresponds
        to a cpe-list element.
        In this case, the opening tag is analyzed.

        :param string name: The opening tag name of an element
        :param Atributes attributes: List of element attributes
        :returns: Returns True if the input opening tag corresponds to a
        cpe-list element
        :rtype: boolean
        """

        self.inCpelist = True

        # Save the cpe list element

        timenow = iso8601.datetime.now().isoformat()
        self.cpelist_db = CpeList(name=timenow)
        self.cpelist_db.save()

    def _startGenerator(self, name, attributes):
        """
        Returns True if the input opening tag corresponds
        to a generator element (or some of its subelements).
        In this case, the opening tag is analyzed.

        :param string name: The opening tag name of an element
        :param Atributes attributes: List of element attributes
        :returns: Returns True if the input opening tag corresponds to a
        generator element (or some of its subelements)
        :rtype: boolean
        """

        if self.inCpelist:
            self.inGenerator = True

            # Initializes the dictionary of generator element
            self.generator[self.TAG_PROD_NAME] = ""
            self.generator[self.TAG_PROD_VER] = ""
            self.generator[self.TAG_SCHEMA_VER] = ""
            self.generator[self.TAG_TIMESTAMP] = ""

    def _startCpeItem(self, name, attributes):
        """
        Returns True if the input opening tag corresponds
        to a cpe-item element.
        In this case, the opening tag is analyzed.

        :param string name: The opening tag name of an element
        :param Atributes attributes: List of element attributes
        :returns: Returns True if the input opening tag corresponds to a
        cpe-item element
        :rtype: boolean
        """

        if self.inCpelist:
            self.inCpeitem = True

            name = attributes.get(self.ATT_CPEITEM_NAME)
            self.cpeitem[self.ATT_CPEITEM_NAME] = name

    def _startCpeItem23(self, name, attributes):
        """
        Returns True if the input opening tag corresponds
        to a cpe23-item element.
        In this case, the opening tag is analyzed.

        :param string name: The opening tag name of an element
        :param Atributes attributes: List of element attributes
        :returns: Returns True if the input opening tag corresponds to a
        cpe23-item element
        :rtype: boolean
        """

        if self.inCpeitem:
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
        Returns True if the input opening tag corresponds
        to a title element.
        In this case, the opening tag is analyzed.

        :param string name: The opening tag name of an element
        :param Atributes attributes: List of element attributes
        :returns: Returns True if the input opening tag corresponds to a
        title element
        :rtype: boolean
        """

        if self.inCpeitem:
            self.inTitle = True

            language = attributes.get(self.ATT_TITLE_LANG)
            self.title[self.ATT_TITLE_LANG] = language

    def startElement(self, name, attributes):
        """
        Analyzes the input opening tag of an element.

        :param string name: The tag name
        :param Attributes attributes: List of element attributes
        :returns: None
        """

        # ------ CPE-LIST ------

        if name == self.TAG_CPELIST:
            self._startCpeList(name, attributes)

        # ------ GENERATOR ------

        elif name == self.TAG_GEN:
            self._startGenerator(name, attributes)
        elif name == self.TAG_PROD_NAME:
            if self.inGenerator:
                self.inGenProdName = True
        elif name == self.TAG_PROD_VER:
            if self.inGenerator:
                self.inGenProdVer = True
        elif name == self.TAG_SCHEMA_VER:
            if self.inGenerator:
                self.inGenSchemaVer = True
        elif name == self.TAG_TIMESTAMP:
            if self.inGenerator:
                self.inGenTimestamp = True

        # ------ CPE-ITEM ------

        elif name == self.TAG_CPEITEM:
            self._startCpeItem(name, attributes)

        # ----- CPE23-ITEM -----

        elif name == self.TAG_CPEITEM_23:
            self._startCpeItem23(name, attributes)

        # -------- TITLE -------
        elif name == self.TAG_TITLE:
            self._startTitle(name, attributes)

    def characters(self, chars):
        """
        Analyze the content of XML elements.

        :param string chars: The content of element as string
        :returns: None
        """

        # ------ GENERATOR ------

        if self.inGenerator:
            if self.inGenProdName:
                self.generator[self.TAG_PROD_NAME] = chars
            if self.inGenProdVer:
                self.generator[self.TAG_PROD_VER] = chars
            if self.inGenSchemaVer:
                self.generator[self.TAG_SCHEMA_VER] = chars
            if self.inGenTimestamp:
                self.generator[self.TAG_TIMESTAMP] = chars

        # -------- TITLE -------

        elif self.inCpeitem:
            if self.inTitle:
                self.title[self.TAG_TITLE] = chars

    def _endGenerator(self, name):
        """
        Returns True if the input ending tag
        corresponds to a generator element (or some of its subelements).
        In this case, the ending tag is analyzed.

        :param string name: The ending tag name of an element
        :returns: Returns True if the input ending tag corresponds to a
        generator element (or some of its subelements)
        :rtype: boolean
        """

        if self.inCpelist:
            self.inGenerator = False

            # Save the generator element

            pn = self.generator[self.TAG_PROD_NAME]
            pv = self.generator[self.TAG_PROD_VER]
            sv = self.generator[self.TAG_SCHEMA_VER]
            ts = self.generator[self.TAG_TIMESTAMP]

            gen = Generator(product_name=pn,
                            product_version=pv,
                            schema_version=sv,
                            timestamp=ts,
                            cpelist=self.cpelist_db)
            gen.save()

    def _endCpeItem(self, name):
        """
        Returns True if the input ending tag corresponds to a cpe-item element.
        In this case, the ending tag is analyzed.

        :param string name: The ending tag name of an element
        :returns: Returns True if the input ending tag corresponds to a
        cpe-item element
        :rtype: boolean
        """

        if self.inCpelist:
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

                    self.cpeitem_db = CpeItem(deprecated=depre,
                                              deprecation_date=depdate,
                                              name=cpedata,
                                              cpelist=self.cpelist_db)
                    self.cpeitem_db.save()

                    if len(self.title) > 0:
                        # Title element must be saved after cpeitem element
                        # because of the dependency between each other
                        title = self.title[self.TAG_TITLE]
                        language = self.title[self.ATT_TITLE_LANG]

                        self.title_db = Title(title=title,
                                              language=language,
                                              cpeitem=self.cpeitem_db)
                        self.title_db.save()

    def _endTitle(self, name):
        """
        Returns True if the input ending tag corresponds to a title element.
        In this case, the ending tag is analyzed.

        :param string name: The ending tag name of an element
        :returns: Returns True if the input ending tag corresponds to a
        title element
        :rtype: boolean
        """

        if self.inCpelist:
            self.inTitle = False

    def endElement(self, name):
        """
        Analyzes the input ending tag of an element.

        :param string name: The tag name
        :returns: None
        """

        # ------ CPE-LIST ------

        if name == self.TAG_CPELIST:
            self.inCpelist = False

        # ----- GENERATOR ------

        elif name == self.TAG_GEN:
            self._endGenerator(name)
        elif name == self.TAG_PROD_NAME:
            if self.inGenerator:
                self.inGenProdName = False
        elif name == self.TAG_PROD_VER:
            if self.inGenerator:
                self.inGenProdVer = False
        elif name == self.TAG_SCHEMA_VER:
            if self.inGenerator:
                self.inGenSchemaVer = False
        elif name == self.TAG_TIMESTAMP:
            if self.inGenerator:
                self.inGenTimestamp = False

        # ------ CPE-ITEM ------

        elif name == self.TAG_CPEITEM:
            self._endCpeItem(name)

        # ------- TITLE --------

        elif name == self.TAG_TITLE:
            self._endTitle(name)
