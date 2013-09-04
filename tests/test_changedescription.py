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

from djangocpe.models import ChangeDescription, ProvenanceRecord
from djangocpe.models import EVIDENCE_CURATOR_UPDATE, CHANGE_ORIGINAL_RECORD
from .fixtures import good_org


@pytest.mark.django_db
class TestChangeDescription:
    """
    Tests to check operations with change description elements
    of CPE dictionary model.
    """

    def test_good_changedescription(self, good_org):
        """
        Check the creation of a correct change description element.
        """

        # Create element
        good_org.full_clean()
        good_org.save()

        prov = mommy.make(ProvenanceRecord, submitter=good_org)

        change_type = CHANGE_ORIGINAL_RECORD
        evidence = EVIDENCE_CURATOR_UPDATE
        datetime = timezone.now()
        comment = "Comment of change description"

        desc = ChangeDescription(change_type=change_type,
                                 datetime=datetime,
                                 evidence_ref=evidence,
                                 comment=comment,
                                 prov_record=prov)
        # Element validation
        desc.full_clean()

        # Save element in database
        desc.save()

        # Load elem from database
        desc_db = ChangeDescription.objects.get(change_type=desc.change_type,
                                                datetime=desc.datetime,
                                                evidence_ref=desc.evidence_ref,
                                                comment=desc.comment,
                                                prov_record=prov)

        assert desc.id == desc_db.id

    def test_bad_changedescription_change_type(self, good_org):
        """
        Check the creation of a change description element
        with an invalid change type.
        """

        # Create element
        good_org.full_clean()
        good_org.save()

        prov = mommy.make(ProvenanceRecord, submitter=good_org)

        # TODO const please instead of 1
        change_type = -1
        evidence = EVIDENCE_CURATOR_UPDATE
        datetime = timezone.now()
        comment = "Comment of change description"

        desc = ChangeDescription(change_type=change_type,
                                 datetime=datetime,
                                 evidence_ref=evidence,
                                 comment=comment,
                                 prov_record=prov)

        # Element validation
        with pytest.raises(ValidationError) as e:
            desc.full_clean()

        assert 'change_type' in e.value.message_dict
        assert 'evidence_ref' not in e.value.message_dict

    def test_bad_changedescription_evidence(self, good_org):
        """
        Check the creation of a change description element
        with an invalid evidence reference.
        """

        # Create element
        good_org.full_clean()
        good_org.save()

        prov = mommy.make(ProvenanceRecord, submitter=good_org)

        change_type = CHANGE_ORIGINAL_RECORD
        # TODO change const
        evidence = -1
        datetime = timezone.now()
        comment = "Comment of change description"

        desc = ChangeDescription(change_type=change_type,
                                 datetime=datetime,
                                 evidence_ref=evidence,
                                 comment=comment,
                                 prov_record=prov)

        # Element validation
        with pytest.raises(ValidationError) as e:
            desc.full_clean()

        assert 'change_type' not in e.value.message_dict
        assert 'evidence_ref' in e.value.message_dict
