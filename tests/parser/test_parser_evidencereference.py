# -*- coding: utf-8 -*-

"""
This file is part of django-cpe package.

This module contains the tests to check import operation with the parser
associated with evidence reference elements in a CPE Dictionary version 2.3
as XML file.

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

from djangocpe.models import EvidenceReference
from djangocpe.models import EVIDENCE_CURATOR_UPDATE
from djangocpe.models import EVIDENCE_VENDOR_FIX
from djangocpe.models import EVIDENCE_THIRD_PARTY_FIX

import function_parsing


@pytest.mark.django_db
class TestCpe23EvidenceReference:
    """
    Tests to check import operation with an evidence reference element
    in CPE dictionary as XML file.
    """

    dirpath = "{0}{1}xml{2}".format(os.path.abspath("."), os.sep, os.sep)

    def test_good_evidencereference_three(self):
        """
        Check the import of one evidence reference element.
        """

        # The XML filepath with the CPE Dictionary
        XML_PATH = "{0}cpedict_v2.3_evidencereference.xml".format(self.dirpath)

        # Parse input XML file
        function_parsing.parse_xmlfile(XML_PATH)

        # Check first evidence element
        evitype1 = EVIDENCE_CURATOR_UPDATE
        ref1 = "http://www.emc.com/support/rsa/eops/agents.htm"
        evi1 = EvidenceReference(ref=ref1, evidence=evitype1)

        # Read first evidence element stored in database
        evi1_list = EvidenceReference.objects.filter(
            ref=evi1.ref, evidence=evi1.evidence)

        evi_db1 = evi1_list[0]

        # Check if test evidence element is stored in database
        assert evi_db1.ref == evi1.ref
        assert evi_db1.evidence == evi1.evidence

        # Check second evidence element
        evitype2 = EVIDENCE_VENDOR_FIX
        ref2 = "https://rubygems.org/gems/sounder/"
        evi2 = EvidenceReference(ref=ref2, evidence=evitype2)

        # Read second evidence element stored in database
        evi2_list = EvidenceReference.objects.filter(
            ref=evi2.ref, evidence=evi2.evidence)

        evi_db2 = evi2_list[0]

        # Check if test evidence element is stored in database
        assert evi_db2.ref == evi2.ref
        assert evi_db2.evidence == evi2.evidence

        # Check third evidence element
        evitype3 = EVIDENCE_THIRD_PARTY_FIX
        ref3 = "https://cpe.mitre.org/"
        evi3 = EvidenceReference(ref=ref3, evidence=evitype3)

        # Read third evidence element stored in database
        evi3_list = EvidenceReference.objects.filter(
            ref=evi3.ref, evidence=evi3.evidence)

        evi_db3 = evi3_list[0]

        # Check if test evidence element is stored in database
        assert evi_db3.ref == evi3.ref
        assert evi_db3.evidence == evi3.evidence
