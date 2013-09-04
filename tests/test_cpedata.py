#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is part of django-cpe package.

This module contains the tests to check operations of CPE data elements of
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
import copy

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from model_mommy import mommy

from djangocpe.models import CpeData
from .fixtures import good_cpedata


@pytest.mark.django_db
class TestCpeData:
    """
    Tests to check operations with cpe data elements
    of CPE dictionary model.
    """

    def test_good_cpe(self):
        """
        Check the creation of a correct cpe data element.
        """

        # Create values
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

        # Create object
        cpe = CpeData(part=part, vendor=vendor, product=product,
                      version=version, update=update, edition=edition,
                      sw_edition=sw_edition, target_sw=target_sw,
                      target_hw=target_hw, other=other, language=language)

        # Object validation
        cpe.full_clean()

        # Save object in database
        cpe.save()

        # Load elem from database
        cpe_db = CpeData.objects.get(part=part, vendor=vendor, product=product,
                                     version=version, update=update,
                                     edition=edition, sw_edition=sw_edition,
                                     target_sw=target_sw, target_hw=target_hw,
                                     other=other, language=language)

        # Compare values
        assert part == cpe_db.part
        assert vendor == cpe_db.vendor
        assert product == cpe_db.product
        assert version == cpe_db.version
        assert update == cpe_db.update
        assert edition == cpe_db.edition
        assert sw_edition == cpe_db.sw_edition
        assert target_sw == cpe_db.target_sw
        assert target_hw == cpe_db.target_hw
        assert other == cpe_db.other
        assert language == cpe_db.language

    def test_good_cpe_empty(self):
        """
        Check the creation of a correct cpe data element.
        """

        # Save elem in database
        cpe = CpeData()

        cpe.full_clean()  # Object validation
        cpe.save()

    def test_bad_cpe_part(self, good_cpedata):
        """
        Check the creation of a cpe data with an invalid value in
        atributte part.
        """

        cpe = good_cpedata
        cpe.part = '"kk"'

        with pytest.raises(ValidationError):
            cpe.full_clean()

    def test_bad_cpe_vendor(self, good_cpedata):
        """
        Check the creation of a cpe data with an invalid value in
        atributte vendor.
        """

        cpe = good_cpedata
        cpe.vendor = '"*??nvidia"'

        with pytest.raises(ValidationError):
            cpe.full_clean()

    def test_bad_cpe_product(self, good_cpedata):
        """
        Check the creation of a cpe data with an invalid value in
        atributte product.
        """

        cpe = good_cpedata
        cpe.product = '"python**"'

        with pytest.raises(ValidationError):
            cpe.full_clean()

    def test_bad_cpe_version(self, good_cpedata):
        """
        Check the creation of a cpe data with an invalid value in
        atributte version.
        """

        cpe = good_cpedata
        cpe.version = '"10.0.1"'

        with pytest.raises(ValidationError):
            cpe.full_clean()

    def test_bad_cpe_update(self, good_cpedata):
        """
        Check the creation of a cpe data with an invalid value in
        atributte update.
        """

        cpe = good_cpedata
        cpe.update = '"update-1"'

        with pytest.raises(ValidationError):
            cpe.full_clean()

    def test_bad_cpe_edition(self, good_cpedata):
        """
        Check the creation of a cpe data with an invalid value in
        atributte edition.
        """

        cpe = good_cpedata
        cpe.edition = 'VA'

        with pytest.raises(ValidationError):
            cpe.full_clean()

    def test_bad_cpe_sw_edition(self, good_cpedata):
        """
        Check the creation of a cpe data with an invalid value in
        atributte sw_edition.
        """

        cpe = good_cpedata
        cpe.sw_edition = '"online**"'

        with pytest.raises(ValidationError):
            cpe.full_clean()

    def test_bad_cpe_target_sw(self, good_cpedata):
        """
        Check the creation of a cpe data with an invalid value in
        atributte target_sw.
        """

        cpe = good_cpedata
        cpe.target_sw = "NAN"

        with pytest.raises(ValidationError):
            cpe.full_clean()

    def test_bad_cpe_target_hw(self, good_cpedata):
        """
        Check the creation of a cpe data with an invalid value in
        atributte target_hw.
        """

        cpe = good_cpedata
        cpe.target_hw = "NAN"

        with pytest.raises(ValidationError):
            cpe.full_clean()

    def test_bad_cpe_other(self, good_cpedata):
        """
        Check the creation of a cpe data with an invalid value in
        atributte other.
        """

        cpe = good_cpedata
        cpe.other = "AANY"

        with pytest.raises(ValidationError):
            cpe.full_clean()

    def test_bad_cpe_language(self, good_cpedata):
        """
        Check the creation of a cpe data with an invalid value in
        atributte language.
        """

        cpe = good_cpedata
        cpe.language = '"en-us"'

        with pytest.raises(ValidationError):
            cpe.full_clean()

    def test_cpe_repeated(self, good_cpedata):
        """
        Check the creation of a cpe data with an invalid value in
        atributte language.
        """

        cpe = good_cpedata
        cperep = copy.deepcopy(good_cpedata)

        cpe.full_clean()
        cpe.save()

        with pytest.raises(IntegrityError):
            cperep.save()
