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

from django.conf.urls import patterns, url, include
from rest_framework import routers
from djangocpe import api


# Routers for API
router = routers.DefaultRouter()
router.register(r'cpedata', api.CpeDataViewSet)

urlpatterns = patterns(
    '',
    # API
    # Base URLs
    url(r'^apicpe/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
)
