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

    part = u'"a"'
    vendor = u'"microsoft"'
    product = u'"internet_explorer"'
    version = u'"10\.0"'
    update = u'"alpha"'
    edition = u'ANY'
    sw_edition = u'NA'
    target_sw = u'ANY'
    target_hw = u'"x64"'
    other = u'NA'
    language = u'"es\-es"'

    return CpeData(part=part, vendor=vendor, product=product,
                   version=version, update=update, edition=edition,
                   sw_edition=sw_edition, target_sw=target_sw,
                   target_hw=target_hw, other=other, language=language)


@pytest.fixture
def good_org():
    """
    Returns a valid organization object.
    """

    suri = u"http://cpe.mitre.org"
    name = u"Mitre Corporation"
    dt = timezone.now()
    desc = u"This organization supports the CPE specification"

    return Organization(system_id=suri,
                        name=name,
                        action_datetime=dt,
                        description=desc)


@pytest.fixture
def good_evidence():
    """
    Return a valid evidence object.
    """

    ref = u"http://evidence.mitre.org"
    evidence = EVIDENCE_CURATOR_UPDATE

    return EvidenceReference(ref=ref, evidence=evidence)
