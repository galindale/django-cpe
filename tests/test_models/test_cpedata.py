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
import unittest
import copy

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from model_mommy import mommy

from djangocpe.models import CpeData
from fixtures_models import good_cpedata


@pytest.mark.django_db
@pytest.mark.models
class TestCpeData(unittest.TestCase):
    """
    Tests to check operations with cpe data elements
    of CPE dictionary model.
    """

    KEY_ATT_PRODUCT = u'product'
    KEY_ATT_VERSION = u'version'
    KEY_ATT_UPDATE = u'update'
    KEY_ATT_EDITION = u'edition'
    KEY_ATT_SW_EDITION = u'sw_edition'
    KEY_ATT_TARGET_SW = u'target_sw'
    KEY_ATT_TARGET_HW = u'target_hw'
    KEY_ATT_OTHER = u'other'
    KEY_ATT_LANGUAGE = u'language'

    def shortDescription(self):
        """
        Overrides the docstring output in nosetest,
        showing the method's name instead
        """

        return None

    def test_good_cpedata_all_fields(self):
        """
        Check the creation of a correct cpe data element
        with all fields filled.
        """

        # Create values
        part = u'"a"'
        vendor = u'"microsoft"'
        product = u'"internet_explorer"'
        version = u'"8\.0"'
        update = u'"beta"'
        edition = u'ANY'
        sw_edition = u'ANY'
        target_sw = u'ANY'
        target_hw = u'"x64"'
        other = u'NA'
        language = u'"es\-es"'

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
        cpe_db = CpeData.objects.get(
            part=cpe.part,
            vendor=cpe.vendor,
            product=cpe.product,
            version=cpe.version,
            update=cpe.update,
            edition=cpe.edition,
            sw_edition=cpe.sw_edition,
            target_sw=cpe.target_sw,
            target_hw=cpe.target_hw,
            other=cpe.other,
            language=cpe.language)

        # Compare values
        assert cpe.id == cpe_db.id
        assert cpe.part == cpe_db.part
        assert cpe.vendor == cpe_db.vendor
        assert cpe.product == cpe_db.product
        assert cpe.version == cpe_db.version
        assert cpe.update == cpe_db.update
        assert cpe.edition == cpe_db.edition
        assert cpe.sw_edition == cpe_db.sw_edition
        assert cpe.target_sw == cpe_db.target_sw
        assert cpe.target_hw == cpe_db.target_hw
        assert cpe.other == cpe_db.other
        assert cpe.language == cpe_db.language

        # Delete cpe created
        cpe_db.delete()

    def test_good_cpedata_min_fields(self):
        """
        Check the creation of a correct cpe data element
        with only required fields filled.
        """

        # Create object
        cpe = mommy.prepare(CpeData)

        # Object validation
        cpe.full_clean()

        # Save object in database
        cpe.save()

        # Load elem from database
        cpe_db = CpeData.objects.get(
            part=cpe.part,
            vendor=cpe.vendor,
            product=cpe.product,
            version=cpe.version,
            update=cpe.update,
            edition=cpe.edition,
            sw_edition=cpe.sw_edition,
            target_sw=cpe.target_sw,
            target_hw=cpe.target_hw,
            other=cpe.other,
            language=cpe.language)

        # Compare values
        assert cpe.id == cpe_db.id
        assert cpe.part == cpe_db.part
        assert cpe.vendor == cpe_db.vendor
        assert cpe.product == cpe_db.product
        assert cpe.version == cpe_db.version
        assert cpe.update == cpe_db.update
        assert cpe.edition == cpe_db.edition
        assert cpe.sw_edition == cpe_db.sw_edition
        assert cpe.target_sw == cpe_db.target_sw
        assert cpe.target_hw == cpe_db.target_hw
        assert cpe.other == cpe_db.other
        assert cpe.language == cpe_db.language

        # Delete cpe created
        cpe_db.delete()

    def test_bad_cpedata_part(self):
        """
        Check the creation of a cpe data with an invalid value in
        atributte part.
        """

        cpe = good_cpedata()
        cpe.part = u'"kk"'

        with pytest.raises(ValidationError) as e:
            cpe.full_clean()

        # Message_dict attribute contains a key '__all__'
        # with the error message associated with the invalid field
        # It is not possible to know what field is bad
        assert len(e.value.message_dict) == 1

    def test_bad_cpedata_vendor(self):
        """
        Check the creation of a cpe data with an invalid value in
        atributte vendor.
        """

        cpe = good_cpedata()
        cpe.vendor = u'"*??nvidia"'

        with pytest.raises(ValidationError) as e:
            cpe.full_clean()

        # Message_dict attribute contains a key '__all__'
        # with the error message associated with the invalid field
        # It is not possible to know what field is bad
        assert len(e.value.message_dict) == 1

    def test_bad_cpedata_product(self):
        """
        Check the creation of a cpe data with an invalid value in
        atributte product.
        """

        cpe = good_cpedata()
        cpe.product = u'"python**"'

        with pytest.raises(ValidationError) as e:
            cpe.full_clean()

        assert self.KEY_ATT_PRODUCT in e.value.message_dict

    def test_bad_cpedata_version(self):
        """
        Check the creation of a cpe data with an invalid value in
        atributte version.
        """

        cpe = good_cpedata()
        cpe.version = '"10.0.1"'

        with pytest.raises(ValidationError) as e:
            cpe.full_clean()

        assert self.KEY_ATT_VERSION in e.value.message_dict

    def test_bad_cpedata_update(self):
        """
        Check the creation of a cpe data with an invalid value in
        atributte update.
        """

        cpe = good_cpedata()
        cpe.update = '"update-1"'

        with pytest.raises(ValidationError) as e:
            cpe.full_clean()

        assert self.KEY_ATT_UPDATE in e.value.message_dict

    def test_bad_cpedata_edition(self):
        """
        Check the creation of a cpe data with an invalid value in
        atributte edition.
        """

        cpe = good_cpedata()
        cpe.edition = 'VA'

        with pytest.raises(ValidationError) as e:
            cpe.full_clean()

        assert self.KEY_ATT_EDITION in e.value.message_dict

    def test_bad_cpedata_sw_edition(self):
        """
        Check the creation of a cpe data with an invalid value in
        atributte sw_edition.
        """

        cpe = good_cpedata()
        cpe.sw_edition = '"online**"'

        with pytest.raises(ValidationError) as e:
            cpe.full_clean()

        assert self.KEY_ATT_SW_EDITION in e.value.message_dict

    def test_bad_cpedata_target_sw(self):
        """
        Check the creation of a cpe data with an invalid value in
        atributte target_sw.
        """

        cpe = good_cpedata()
        cpe.target_sw = "NAN"

        with pytest.raises(ValidationError) as e:
            cpe.full_clean()

        assert self.KEY_ATT_TARGET_SW in e.value.message_dict

    def test_bad_cpedata_target_hw(self):
        """
        Check the creation of a cpe data with an invalid value in
        atributte target_hw.
        """

        cpe = good_cpedata()
        cpe.target_hw = "NAN"

        with pytest.raises(ValidationError) as e:
            cpe.full_clean()

        assert self.KEY_ATT_TARGET_HW in e.value.message_dict

    def test_bad_cpedata_other(self):
        """
        Check the creation of a cpe data with an invalid value in
        atributte other.
        """

        cpe = good_cpedata()
        cpe.other = "AANY"

        with pytest.raises(ValidationError) as e:
            cpe.full_clean()

        assert self.KEY_ATT_OTHER in e.value.message_dict

    def test_bad_cpedata_language(self):
        """
        Check the creation of a cpe data with an invalid value in
        atributte language.
        """

        cpe = good_cpedata()
        cpe.language = '"en-us"'

        with pytest.raises(ValidationError) as e:
            cpe.full_clean()

        assert self.KEY_ATT_LANGUAGE in e.value.message_dict

    def test_cpedata_repeated(self):
        """
        Check the creation of a cpe data with an invalid value in
        atributte language.
        """

        cpe = good_cpedata()
        cperep = copy.deepcopy(cpe)

        cpe.full_clean()
        cpe.save()

        with pytest.raises(IntegrityError):
            cperep.save()

        cpe.delete()
