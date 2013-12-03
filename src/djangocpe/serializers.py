# -*- coding: utf-8 -*-

from djangocpe.models import CpeData
from rest_framework import serializers


class CpeDataSerializer(serializers.HyperlinkedModelSerializer):

    """
    Serializes cpe data to work with the API.
    """

    class Meta:
        """
        Meta options used by the CpeDataSerializer.
        """

        #: Model used by the serializer
        model = CpeData

        #: Fields to be serialized
        fields = ('id', 'part', 'vendor', 'product', 'version', 'update',
                  'edition', 'sw_edition', 'target_sw', 'target_hw', 'other',
                  'language', )

        #: Serialized read only fields
        read_only_fields = ('id', )
