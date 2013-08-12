# -*- coding: utf-8 -*-

# from cpe import CPE
from django.core.exceptions import ValidationError
from django.db import models

import rfc3987 as rfc

from cpe import CPE


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
        """

        try:
            rfc.parse(value, rule='URI')
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
        """

        # TODO: improve validation and not use CPE package
        cpename = 'cpe:/a:mozilla:firefox:22::osx:{0}'.format(value)
        try:
            CPE(cpename)
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
