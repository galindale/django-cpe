#!/usr/bin/env python
#-*- coding: utf-8 -*-

u"""py.test fixtures for django-cpe."""

import pytest
from django.utils import timezone

from djangocpe.models import CpeData, Organization, EvidenceReference
from djangocpe.models import EVIDENCE_CURATOR_UPDATE


@pytest.fixture
def good_cpedata():
    """
    Returns a valid cpe data object with information about a CPE Name.
    """

    part = '"a"'
    vendor = '"microsoft"'
    product = '"internet_explorer"'
    version = '"10\.0"'
    update = '"alpha"'
    edition = 'ANY'
    sw_edition = 'NA'
    target_sw = 'ANY'
    target_hw = '"x64"'
    other = 'NA'
    language = '"es\-es"'

    return CpeData(part=part, vendor=vendor, product=product,
                   version=version, update=update, edition=edition,
                   sw_edition=sw_edition, target_sw=target_sw,
                   target_hw=target_hw, other=other, language=language)


@pytest.fixture
def good_org():
    """
    Returns a valid organization object.
    """

    suri = "http://cpe.mitre.org"
    name = "Mitre Corporation"
    dt = timezone.now()
    desc = "This organization supports the CPE specification"

    return Organization(system_id=suri,
                        name=name,
                        action_datetime=dt,
                        description=desc)


@pytest.fixture
def good_evidence():
    """
    Return a valid evidence object.
    """

    ref = "http://evidence.mitre.org"
    evidence = EVIDENCE_CURATOR_UPDATE

    return EvidenceReference(ref=ref, evidence=evidence)
