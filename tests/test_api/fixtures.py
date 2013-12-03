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
def create_cpedata(num):
    """
    Create the input count of cpe data in database.
    """

    part = '"a"'
    vendor = '"microsoft"'
    product = '"internet_explorer"'
    update = '"alpha"'
    edition = 'ANY'
    sw_edition = 'NA'
    target_sw = 'ANY'
    target_hw = '"x64"'
    other = 'NA'
    language = '"es\-es"'

    for i in range(0,num):
        version = '"{0}\.0"'.format(i)
        cpedata = CpeData(part=part, vendor=vendor, product=product,
                          version=version, update=update, edition=edition,
                          sw_edition=sw_edition, target_sw=target_sw,
                          target_hw=target_hw, other=other, language=language)
        cpedata.save()
