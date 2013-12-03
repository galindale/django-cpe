# -*- coding: utf-8 -*-

"""
This file is part of django-cpe package.

This module contains the tests to check import operation with the parser
associated with cpedata values in a CPE Dictionary version 2.3 as XML file.

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

from djangocpe.models import CpeData

import function_parsing


@pytest.mark.django_db
class TestCpe23CpeData:
    """
    Tests to check import operation with a cpedata values
    in CPE dictionary as XML file.
    """

    dirpath = "{0}{1}xml{2}".format(os.path.abspath("."), os.sep, os.sep)

    def _check_cpedata(self, cpedata):
        """
        Get the cpedata values and check if they are saved correctly
        in database.

        :param CpeData cpedata: The values of cpedata
        :returns: None
        """

        # Read cpedata values stored in database
        cpedata_list = CpeData.objects.filter(
            part=cpedata.part,
            vendor=cpedata.vendor,
            product=cpedata.product,
            version=cpedata.version,
            update=cpedata.update,
            edition=cpedata.edition,
            sw_edition=cpedata.sw_edition,
            target_sw=cpedata.target_sw,
            target_hw=cpedata.target_hw,
            other=cpedata.other,
            language=cpedata.language)

        cpedata_db = cpedata_list[0]

        # Check if test cpedata values is stored in database
        assert cpedata_db.part == cpedata.part
        assert cpedata_db.vendor == cpedata.vendor
        assert cpedata_db.product == cpedata.product
        assert cpedata_db.version == cpedata.version
        assert cpedata_db.update == cpedata.update
        assert cpedata_db.edition == cpedata.edition
        assert cpedata_db.sw_edition == cpedata.sw_edition
        assert cpedata_db.target_sw == cpedata.target_sw
        assert cpedata_db.target_hw == cpedata.target_hw
        assert cpedata_db.other == cpedata.other
        assert cpedata_db.language == cpedata.language

    def test_good_cpedata_any_fields(self):
        """
        Check the import of a cpedata with ANY values.
        """

        # The XML filepath with the CPE Dictionary
        XML_PATH = "{0}cpedict_v2.3_cpedata_min_fields.xml".format(
            self.dirpath)

        # Parse input XML file
        function_parsing.parse_xmlfile(XML_PATH)

        # Cpedata values
        part = 'ANY'
        vendor = 'ANY'
        product = 'ANY'
        version = 'ANY'
        update = 'ANY'
        edition = 'ANY'
        sw_edition = 'ANY'
        target_sw = 'ANY'
        target_hw = 'ANY'
        other = 'ANY'
        language = 'ANY'

        cpedata = CpeData(part=part, vendor=vendor, product=product,
                          version=version, update=update, edition=edition,
                          sw_edition=sw_edition, target_sw=target_sw,
                          target_hw=target_hw, other=other, language=language)

        # Check cpedata element
        self._check_cpedata(cpedata)

    def test_good_cpeitem_all_fields(self):
        """
        Check the import of a cpe-item element with all fields filled.
        """

        # The XML filepath with the CPE Dictionary
        XML_PATH = "{0}cpedict_v2.3_cpedata_all_fields.xml".format(
            self.dirpath)

        # Parse input XML file
        function_parsing.parse_xmlfile(XML_PATH)

        # Cpedata values
        part = '"a"'
        vendor = '"microsoft"'
        product = '"internet_explorer"'
        version = '"8\.0"'
        update = '"beta"'
        edition = 'ANY'
        sw_edition = 'ANY'
        target_sw = 'ANY'
        target_hw = '"x64"'
        other = 'NA'
        language = '"es\-es"'

        cpedata = CpeData(part=part, vendor=vendor, product=product,
                          version=version, update=update, edition=edition,
                          sw_edition=sw_edition, target_sw=target_sw,
                          target_hw=target_hw, other=other, language=language)

        # Check cpedata element
        self._check_cpedata(cpedata)
