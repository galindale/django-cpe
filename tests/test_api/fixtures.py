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
def create_cpedata(num):
    """
    Create the input count of cpe data in database.

    :param int num: The amount of cpedata elements to create
    :returns: The cpedata list created
    :rtype: list
    """

    part = u'"a"'
    vendor = u'"microsoft"'
    product = u'"internet_explorer"'
    update = u'"alpha"'
    edition = u'ANY'
    sw_edition = u'NA'
    target_sw = u'ANY'
    target_hw = u'"x64"'
    other = u'NA'
    language = u'"es\-es"'

    cpedata_list = []

    for i in range(0, num):
        version = '"{0}\.0"'.format(i)
        cpedata = CpeData(part=part, vendor=vendor, product=product,
                          version=version, update=update, edition=edition,
                          sw_edition=sw_edition, target_sw=target_sw,
                          target_hw=target_hw, other=other, language=language)
        cpedata.save()
        cpedata_list.append(cpedata)

    return cpedata_list