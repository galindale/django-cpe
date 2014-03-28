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

from rfc3987 import parse

from cpe.cpe import CPE

from django.core.exceptions import ValidationError
from django.db import models


class URIField(models.URLField):
    """
    Field associated with the URI attributes of CPE dictionary model
    with a particular length.
    """

    description = "A Uniform Resource Identifier (URI)"

    def validate_uri(value):
        """
        Check if value is a valid URI according to RFC 3986
        'Uniform Resource Identifier (URI): Generic Syntax'

        :param string value: URI value to check
        :returns: valid URI?
        :rtyoe: boolean
        :exception: ValidationError - Invalid URI value
        """

        try:
            parse(value, rule='URI_reference')
        except ValueError:
            # Incorrect URI
            raise ValidationError(
                message=u'Invalid URI: {0}'.format(value),
                code='invalid'
            )

    default_validators = [validate_uri]

    def __init__(self, *args, **kwargs):
        # Set the field max length independently of input value of attribute
        # 'max_length'
        kwargs['max_length'] = 255

        super(URIField, self).__init__(*args, **kwargs)


class LanguageField(models.CharField):
    """
    Contains the validation behaviour of language fields.
    """

    description = "A language identifier according to standard RFC 5646"

    def validate_lang(value):
        """
        Check if value is a valid language value according to
        standard RFC 5646 'Tags for Identifying Languages'

        :param string value: language value to check
        :returns: valid language?
        :rtyoe: boolean
        :exception: ValidationError - Invalid language value
        """

        # TODO: improve validation and not use CPE package
        cpename = 'cpe:/a:mozilla:firefox:22::osx:{0}'.format(value)
        try:
            CPE(cpename, CPE.VERSION_2_2)
        except (ValueError, NotImplementedError):
            # Incorrect language
            raise ValidationError(
                message=u'Invalid language: {0}'.format(value),
                code='invalid'
            )

    default_validators = [validate_lang]

    def __init__(self, *args, **kwargs):
        # Set the field max length independently of input value of attribute
        # 'max_length'
        kwargs['max_length'] = 255

        super(LanguageField, self).__init__(*args, **kwargs)
