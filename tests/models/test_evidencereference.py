# -*- coding: utf-8 -*-

"""
This file is part of django-cpe package.

This module contains the tests to check operations of evidence reference
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

from django.core.exceptions import ValidationError
from model_mommy import mommy

from djangocpe.models import EvidenceReference
from djangocpe.models import EVIDENCE_CURATOR_UPDATE


@pytest.mark.django_db
class TestEvidenceReference:
    """
    Tests to check operations with evidence reference elements
    of CPE dictionary model.
    """

    #: Bad value in evidence attribute of EvidenceReference model
    BAD_EVIDENCE = -1

    def test_good_evidencereference_all_fields(self):
        """
        Check the creation of a correct evidence reference element
        with all fields filled.
        """

        # Create evidence reference element
        ref = "http://evidence.mitre.org"
        evidence = EVIDENCE_CURATOR_UPDATE

        evi = EvidenceReference(ref=ref, evidence=evidence)

        # Evidence reference element validation
        evi.full_clean()

        # Save evidence reference element in database
        evi.save()

        # Load evidence reference element from database
        evi_db = EvidenceReference.objects.get(
            ref=evi.ref,
            evidence=evi.evidence)

        # Compare values
        assert evi.id == evi_db.id
        assert evi.ref == evi_db.ref
        assert evi.evidence == evi_db.evidence

    def test_bad_evidencereference_ref(self):
        """
        Check the creation of a evidence reference element
        with an invalid ref field.
        """

        evi = mommy.prepare(EvidenceReference, ref="baduri")

        with pytest.raises(ValidationError) as e:
            evi.full_clean()

        assert 'ref' in str(e.value)
        assert 'evidence' not in str(e.value)

    def test_bad_evidencereference_evidence(self):
        """
        Check the creation of a evidence reference element
        with an invalid ref field.
        """

        ref = "http://badevidence.mitre.org"
        evidence = self.BAD_EVIDENCE

        evi = mommy.prepare(EvidenceReference, ref=ref, evidence=evidence)

        with pytest.raises(ValidationError) as e:
            evi.full_clean()

        assert 'ref' not in str(e.value)
        assert 'evidence' in str(e.value)
