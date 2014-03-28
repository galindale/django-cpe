# -*- coding: utf-8 -*-

"""
This file is part of django-cpe package.

This module contains the tests to check operations of change description
elements of CPE dictionary model.

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

from django.utils import timezone
from django.core.exceptions import ValidationError
from model_mommy import mommy

from djangocpe.models import ChangeDescription
from djangocpe.models import ProvenanceRecord
from djangocpe.models import CHANGE_ORIGINAL_RECORD


@pytest.mark.django_db
class TestChangeDescription:
    """
    Tests to check operations with change description elements
    of CPE dictionary model.
    """

    #: Bad value in change type attribute of ChangeDescription model
    BAD_CHANGE_TYPE = -1

    def test_good_changedescription_min_fields(self, good_org):
        """
        Check the creation of a correct change description element
        with only required fields filled.
        """

        # Create organization element
        good_org.full_clean()
        good_org.save()

        # Create ProvenanceRecord element
        prov = mommy.make(ProvenanceRecord, submitter=good_org)

        # Create ChangeDescription element
        change_type = CHANGE_ORIGINAL_RECORD
        dt = timezone.now()

        desc = ChangeDescription(change_type=change_type,
                                 change_datetime=dt,
                                 prov_record=prov)

        # ChangeDescription element validation
        desc.full_clean()

        # Save ChangeDescription element in database
        desc.save()

        # Load ChangeDescription element from database
        desc_db = ChangeDescription.objects.get(
            change_type=desc.change_type,
            change_datetime=desc.change_datetime,
            prov_record=desc.prov_record)

        # Compare values
        assert desc.id == desc_db.id
        assert desc.change_type == desc_db.change_type
        assert desc.change_datetime == desc_db.change_datetime
        assert desc.comment == desc_db.comment
        assert desc.evidence == desc_db.evidence
        assert desc.prov_record == desc_db.prov_record

    def test_good_changedescription_all_fields(self, good_org, good_evidence):
        """
        Check the creation of a correct change description element
        with all fields filled.
        """

        # Create organization element
        good_org.full_clean()
        good_org.save()

        # Create ProvenanceRecord element
        prov = mommy.make(ProvenanceRecord, submitter=good_org)

        # Create evidence element
        good_evidence.full_clean()
        good_evidence.save()

        # Create ChangeDescription element
        change_type = CHANGE_ORIGINAL_RECORD
        dt = timezone.now()
        comment = "Comment of change description"

        desc = ChangeDescription(change_type=change_type,
                                 change_datetime=dt,
                                 comment=comment,
                                 evidence=good_evidence,
                                 prov_record=prov)

        # ChangeDescription element validation
        desc.full_clean()

        # Save ChangeDescription element in database
        desc.save()

        # Load ChangeDescription element from database
        desc_db = ChangeDescription.objects.get(
            change_type=desc.change_type,
            change_datetime=desc.change_datetime,
            comment=desc.comment,
            evidence=desc.evidence,
            prov_record=desc.prov_record)

        # Compare values
        assert desc.id == desc_db.id
        assert desc.change_type == desc_db.change_type
        assert desc.change_datetime == desc_db.change_datetime
        assert desc.comment == desc_db.comment
        assert desc.evidence == desc_db.evidence
        assert desc.prov_record == desc_db.prov_record

    def test_bad_changedescription_change_type(self, good_org, good_evidence):
        """
        Check the creation of a change description element
        with an invalid change type.
        """

        # Create organization element
        good_org.full_clean()
        good_org.save()

        # Create ProvenanceRecord element
        prov = mommy.make(ProvenanceRecord, submitter=good_org)

        # Create evidence element
        good_evidence.full_clean()
        good_evidence.save()

        # Create ChangeDescription element
        change_type = self.BAD_CHANGE_TYPE
        dt = timezone.now()
        comment = "Comment of change description"

        desc = ChangeDescription(change_type=change_type,
                                 change_datetime=dt,
                                 evidence=good_evidence,
                                 comment=comment,
                                 prov_record=prov)

        # Element validation
        with pytest.raises(ValidationError) as e:
            desc.full_clean()

        assert 'change_type' in e.value.message_dict
