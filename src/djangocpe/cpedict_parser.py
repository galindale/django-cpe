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

import sys

from xml.sax import make_parser

from cpedict23_handler import Cpedict23Handler


class CpedictParser(object):
    """
    This class implements a parser that import and export CPE Dictionaries
    specified as XML files.
    """

    def __init__(self, handler):
        """
        Initialize the parser with the input handler.

        :param ContentHandler handler: CPE Dictionary handler
        :returns: None
        """

        self.parser = make_parser()
        self.parser.setContentHandler(handler)

    def parse(self, filepath):
        """
        Execute parsing with the input file.
        """

        self.parser.parse(filepath)

if __name__ == "__main__":
    # TODO: Let both versions 2.2 and 2.3

    handler = Cpedict23Handler()
    parser = make_parser()
    parser.setContentHandler(handler)
    #parser.parse(sys.stdin)
    parser.parse(sys.argv[1])
