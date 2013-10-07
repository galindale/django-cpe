# -*- coding: utf-8 -*-

"""
This file is part of django-cpe package.

This module contains the function to parse XML files associated with
elements in a CPE Dictionary version 2.3 in the test files.
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

from djangocpe.cpedict_parser import CpedictParser
from djangocpe.cpedict23_handler import Cpedict23Handler


def parse_xmlfile(xmlpath):
    """
    Parse the input XML file and save its elements in database.

    :param string xmlpath: The XML filepath with the CPE Dictionary
    :returns: None
    """

    # Set handler
    handler = Cpedict23Handler()
    p = CpedictParser(handler)

    # Execute parser with input XML file
    p.parse(xmlpath)
