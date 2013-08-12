# -*- coding: utf-8 *-*

"""
This file is part of django-cpe package.

This module contains the tests to check operations of provenance reoord
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

from djangocpe.models import ProvenanceRecord, CpeItem
from model_mommy import mommy

from .fixtures import good_org


@pytest.mark.django_db
class TestProvenanceRecord:
    """
    Tests to check operations with provenance record elements
    of CPE dictionary model.
    """

    def test_good_provenance_record(self, good_org):
        """
        Check the creation of a correct provenance record element.
        """

        # Save elem in database
        org = good_org
        org.full_clean()
        org.save()

        prov = mommy.make(ProvenanceRecord, submitter=org)

        # Load elem from database
        prov_db = ProvenanceRecord.objects.get(id=prov.id)

        assert prov.id == prov_db.id
