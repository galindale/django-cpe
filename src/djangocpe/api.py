# -*- coding: utf-8 -*-

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
