# -*- coding: utf-8 -*-

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
