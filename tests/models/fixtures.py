#!/usr/bin/env python
#-*- coding: utf-8 -*-

u"""py.test fixtures for django-cpe."""

import pytest
from django.utils import timezone

from djangocpe.models import CpeData, Organization


@pytest.fixture
def good_cpedata():
    """
    Returns a valid cpe data with information about a CPE Name.
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
    Returns a valid organization.
    """

    # Create values
    suri = "http://cpe.mitre.org"
    name = "Mitre Corporation"
    dt = timezone.now()
    desc = "This organization supports the CPE specification"

    # Save elem in database
    return Organization(system_uri=suri,
                        name=name,
                        datetime_action=dt,
                        description=desc)
