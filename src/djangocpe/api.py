#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is part of django-cpe package.

This module implements the parser that import and export CPE Dictionaries
specified as XML files.

Copyright (C) 2013  Alejandro Galindo Garcí Roberto Abdelkader Martíz Péz

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

- Alejandro Galindo Garcí galindo.garcia.alejandro@gmail.com
- Roberto Abdelkader Martíz Péz: robertomartinezp@gmail.com
"""

from djangocpe import models
from djangocpe import serializers
from rest_framework import viewsets


class CpeDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage CPE data.
    """

    #: QuerySet used to retrieve cpe data
    queryset = models.CpeData.objects.all()

    #: Serializer used by the viewset
    serializer_class = serializers.CpeDataSerializer

    def get_queryset(self):
        """
        Generates the queryset for this viewset
        and filters if there is any param passed
        """

        # QuerySet used to retrieve assets
        queryset = models.CpeData.objects.all()

        # Take part field from GET params
        part = self.request.QUERY_PARAMS.get(
            'part', None)
        if part is not None:
            queryset = queryset.filter(part=part)

        # Take vendor field from GET params
        vendor = self.request.QUERY_PARAMS.get(
            'vendor', None)
        if vendor is not None:
            queryset = queryset.filter(vendor=vendor)

        # Take product field from GET params
        product = self.request.QUERY_PARAMS.get(
            'product', None)
        if product is not None:
            queryset = queryset.filter(product=product)

        # Take version field from GET params
        version = self.request.QUERY_PARAMS.get(
            'version', None)
        if version is not None:
            queryset = queryset.filter(version=version)

        # Take update field from GET params
        update = self.request.QUERY_PARAMS.get(
            'update', None)
        if update is not None:
            queryset = queryset.filter(update=update)

        # Take edition field from GET params
        edition = self.request.QUERY_PARAMS.get(
            'edition', None)
        if edition is not None:
            queryset = queryset.filter(edition=edition)

        # Take sw_edition field from GET params
        sw_edition = self.request.QUERY_PARAMS.get(
            'sw_edition', None)
        if sw_edition is not None:
            queryset = queryset.filter(sw_edition=sw_edition)

        # Take target_sw field from GET params
        target_sw = self.request.QUERY_PARAMS.get(
            'target_sw', None)
        if target_sw is not None:
            queryset = queryset.filter(target_sw=target_sw)

        # Take target_hw field from GET params
        target_hw = self.request.QUERY_PARAMS.get(
            'target_hw', None)
        if target_hw is not None:
            queryset = queryset.filter(target_hw=target_hw)

        # Take other field from GET params
        other = self.request.QUERY_PARAMS.get(
            'other', None)
        if other is not None:
            queryset = queryset.filter(other=other)

        # Take language field from GET params
        language = self.request.QUERY_PARAMS.get(
            'language', None)
        if language is not None:
            queryset = queryset.filter(language=language)

        return queryset
