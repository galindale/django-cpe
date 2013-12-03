# -*- coding: utf-8 -*-

"""
This file is part of package django-cpe.

This module contains the tests to validate CPE data API interaction.
"""

import pytest
import requests
import json
import unittest
from model_mommy import mommy
from djangocpe.models import CpeData
from django.conf import settings
from fixtures import good_cpedata


class TestCpeDataApi(unittest.TestCase):

    #: Base host where the API endpoint is exposed
    BASE_HOST = u'http://20.1.40.228'

    #: Base port where the API endpoint is exposed
    BASE_PORT = u'8000'

    #: Base port where the API endpoint is exposed
    BASE_API_URL = u'/apicpe/cpedata/'

    #: HTTP Header to retrieve a JSON
    JSON_HEADER = {u'content-type': u'application/json'}

    #: Dictionary key associated with JSON results
    KEY_RESULTS = u"results"

    #: Dictionary key associated with JSON actions
    KEY_ACTIONS = u"actions"

    #: Dictionary key associated with JSON header allow
    KEY_HEADER_ALLOW = u"allow"

    #: Dictionary key associated with JSON data count
    KEY_COUNT = u"count"

    #: Dictionary key associated with JSON data pagination
    KEY_PAGINATED_BY = u"PAGINATE_BY"

    # ------ JSON methods ------

    #: Dictionary key associated with JSON GET method
    KEY_METHOD_GET = u"GET"

    #: Dictionary key associated with JSON HEAD method
    KEY_METHOD_HEAD = u"HEAD"

    #: Dictionary key associated with JSON POST method
    KEY_METHOD_OPTIONS = u"POST"

    #: Dictionary key associated with JSON OPTIONS method
    KEY_METHOD_POST = u"OPTIONS"

    #: Dictionary key associated with JSON PUT method
    KEY_METHOD_PUT = u"PUT"

    # ------ model fields ------

    #: Dictionary key associated with model field id
    KEY_ATT_ID = u"id"

    #: Dictionary key associated with model field part
    KEY_ATT_PART = u"part"

    #: Dictionary key associated with model field vendor
    KEY_ATT_VENDOR = u"vendor"

    #: Dictionary key associated with model field product
    KEY_ATT_PRODUCT = u"product"

    #: Dictionary key associated with model field version
    KEY_ATT_VERSION = u"version"

    #: Dictionary key associated with model field update
    KEY_ATT_UPDATE = u"update"

    #: Dictionary key associated with model field edition
    KEY_ATT_EDITION = u"edition"

    #: Dictionary key associated with model field sw_edition
    KEY_ATT_SW_EDITION = u"sw_edition"

    #: Dictionary key associated with model field target_sw
    KEY_ATT_TARGET_SW = u"target_sw"

    #: Dictionary key associated with model field target_hw
    KEY_ATT_TARGET_HW = u"target_hw"

    #: Dictionary key associated with model field other
    KEY_ATT_OTHER = u"other"

    #: Dictionary key associated with model field language
    KEY_ATT_LANGUAGE = u"language"

    # def __init__(self):
        # """
        # Read the initial data of test.
        # """

        # self.endpoint = '{host}:{port}{api_url}'.format(
            # host=self.BASE_HOST,
            # port=self.BASE_PORT,
            # api_url=self.BASE_API_URL)

    def shortDescription(self):
        """
        Overrides the doctring output in nosetest,
        showing the method's name instead
        """

        return None

    @pytest.mark.api
    def test_cpedata_list_options(self):
        """
        Checks the cpe data list OPTIONS method in the API,
        checks the allowed methods and that the schema is present.
        """

        # Retrieve OPTIONS from API
        endpoint = '{host}:{port}{api_url}'.format(
            host=self.BASE_HOST,
            port=self.BASE_PORT,
            api_url=self.BASE_API_URL)

        options_request = requests.options(
            endpoint, headers=self.JSON_HEADER)

        # Check HTTP Status Code is OK (200)
        assert options_request.status_code == requests.codes.ok

        options = options_request.json()

        # Check allowed methods in headers
        methods = options_request.headers[self.KEY_HEADER_ALLOW].split(', ')

        # Check that necessary methods are allowed
        assert self.KEY_METHOD_GET in methods
        assert self.KEY_METHOD_POST in methods
        assert self.KEY_METHOD_HEAD in methods
        assert self.KEY_METHOD_OPTIONS in methods

        # If we have POST it means that we can create.
        # Let's verify that we have a list of fields for POST
        assert options[self.KEY_ACTIONS].get(self.KEY_METHOD_POST) is not None

    @pytest.mark.api
    def test_cpedata_list_with_default_limit(self):
        """
        Checks the listing of cpe data via api using
        the actual limit of the resource (default: 20).
        """

        # Generate 20 mommys to test
        cpedata_list = create_cpedata(20)

        # Retrieve cpe data from API
        endpoint = '{host}:{port}{api_url}'.format(
            host=self.BASE_HOST,
            port=self.BASE_PORT,
            api_url=self.BASE_API_URL)

        list_request = requests.get(
            endpoint, headers=self.JSON_HEADER)

        # Check HTTP Status Code is OK (200)
        assert list_request.status_code == requests.codes.ok

        data = list_request.json()
        results = data.get(self.KEY_RESULTS)

        # Check that JSON contains main data block (results)
        assert results is not None

        # Check that number of results are less
        # or equal than the limit in settings
        assert len(results) <= settings.REST_FRAMEWORK[self.KEY_PAGINATED_BY]

        db_objects = CpeData.objects.all()

        # Check that total count in API equals total count in model
        assert data[self.KEY_COUNT] == len(cpedata_list)

        for cpe in cpedata_list:
            cpe.delete()

    @pytest.mark.api
    def test_cpedata_list_with_more_than_one_page(self):
        """
        Checks the listing of controls via api
        with a limit less than total count
        to check correct pagination.
        """

        # Generate 20 mommys to test
        cpedata_list = create_cpedata(20)

        # Retrieve controls from API
        endpoint = u'{host}:{port}{api_url}'.format(
            host=self.BASE_HOST,
            port=self.BASE_PORT,
            api_url=self.BASE_API_URL)
        params = {u'limit': 10}  # Limit should be less than quantity of mommys
        list_request = requests.get(
            endpoint, headers=self.JSON_HEADER, params=params)

        # Check HTTP Status Code is OK (200)
        assert list_request.status_code == requests.codes.ok

        data = list_request.json()
        results = data.get(self.KEY_RESULTS)

        # Check that JSON contains main data block (results)
        assert results is not None

        # Check that meta contains a next URI
        next_uri = data.get(u'next')
        assert next_uri is not None

        # Retrieve next page from API
        list_request_next = requests.get(
            next_uri, headers=self.JSON_HEADER)

        # Check HTTP Status Code is OK (200) (Next Page)
        assert list_request_next.status_code == requests.codes.ok

        data_next = list_request_next.json()
        results_next = data_next.get(self.KEY_RESULTS)

        # Check that JSON contains main data block (results)
        assert results_next is not None

        # Check that next page contains a prev URI
        prev_uri = data_next.get(u'previous')
        assert prev_uri is not None

        # Retrieve original page from API via prev URI in next page
        list_request_prev = requests.get(
            prev_uri, headers=self.JSON_HEADER)

        # Check HTTP Status Code is OK (200) (Previous Page)
        assert list_request_prev.status_code == requests.codes.ok

        data_prev = list_request_prev.json()
        results_prev = data_prev.get(self.KEY_RESULTS)

        # Check that JSON contains main data block (results)
        assert results_prev is not None

        # Check that objects from previous page
        # equals that from original request
        assert results_prev == results

        for cpe in cpedata_list:
            cpe.delete()

    @pytest.mark.api
    def test_cpedata_list_post_new_good_min_fields(self):
        """
        Checks the creation of a new cpe data
        via API including minimum fields required
        """

        json_cpedata = {self.KEY_ATT_PART: u'"a"',
                        self.KEY_ATT_VENDOR: u'"microsoft"',
                        self.KEY_ATT_PRODUCT: u'"internet_explorer"',
                        self.KEY_ATT_VERSION: u'"8\.0"',
                        self.KEY_ATT_UPDATE: u'"beta"',
                        self.KEY_ATT_EDITION: u'ANY',
                        self.KEY_ATT_SW_EDITION: u'ANY',
                        self.KEY_ATT_TARGET_SW: u'ANY',
                        self.KEY_ATT_TARGET_HW: u'"x64"',
                        self.KEY_ATT_OTHER: u'NA',
                        self.KEY_ATT_LANGUAGE: u'"es\-es"',
                        }

        endpoint = u'{host}:{port}{api_url}'.format(
            host=self.BASE_HOST,
            port=self.BASE_PORT,
            api_url=self.BASE_API_URL)

        new_request = requests.post(
            endpoint,
            headers=self.JSON_HEADER,
            data=json.dumps(json_cpedata))

        # Check HTTP Status Code is Created (201)
        assert new_request.status_code == requests.codes.created

        json_created = new_request.json()

        # Check values from API response are equal to that we sent
        assert json_cpedata[self.KEY_ATT_PART] == json_created[self.KEY_ATT_PART]
        assert json_cpedata[self.KEY_ATT_VENDOR] == json_created[self.KEY_ATT_VENDOR]
        assert json_cpedata[self.KEY_ATT_PRODUCT] == json_created[self.KEY_ATT_PRODUCT]
        assert json_cpedata[self.KEY_ATT_VERSION] == json_created[self.KEY_ATT_VERSION]
        assert json_cpedata[self.KEY_ATT_UPDATE] == json_created[self.KEY_ATT_UPDATE]
        assert json_cpedata[self.KEY_ATT_EDITION] == json_created[self.KEY_ATT_EDITION]
        assert json_cpedata[self.KEY_ATT_SW_EDITION] == json_created[self.KEY_ATT_SW_EDITION]
        assert json_cpedata[self.KEY_ATT_TARGET_SW] == json_created[self.KEY_ATT_TARGET_SW]
        assert json_cpedata[self.KEY_ATT_TARGET_HW] == json_created[self.KEY_ATT_TARGET_HW]
        assert json_cpedata[self.KEY_ATT_OTHER] == json_created[self.KEY_ATT_OTHER]
        assert json_cpedata[self.KEY_ATT_LANGUAGE] == json_created[self.KEY_ATT_LANGUAGE]

        # Delete created control
        CpeData.objects.get(id=json_created[self.KEY_ATT_ID]).delete()

    @pytest.mark.api
    def test_cpedata_list_post_new_bad_required_fields(self):
        """
        Checks the error during creation of a new control
        without all the required fields
        """

        json_cpedata = {self.KEY_ATT_PART: u''}

        endpoint = u'{host}:{port}{api_url}'.format(
            host=self.BASE_HOST,
            port=self.BASE_PORT,
            api_url=self.BASE_API_URL)

        new_request = requests.post(
            endpoint,
            headers=self.JSON_HEADER,
            data=json.dumps(json_cpedata))

        # Check HTTP Status Code is Bad Request (400)
        assert new_request.status_code == requests.codes.bad_request

        error_list = new_request.json()

        # Check if the error list has errors for incomplete fields
        assert error_list.get(self.KEY_ATT_PART) is not None

    @pytest.mark.api
    def test_cpedata_details_options(self):
        """
        Checks the cpe data details OPTIONS method
        checks the allowed methods and that the schema is present
        """

        # Create a cpe data
        cpedata = good_cpedata()
        cpedata.save()

        # Retrieve OPTIONS from API
        endpoint = u'{host}:{port}{api_url}{cpedata_pk}/'.format(
            host=self.BASE_HOST,
            port=self.BASE_PORT,
            api_url=self.BASE_API_URL,
            cpedata_pk=cpedata.pk)
        options_request = requests.options(
            endpoint, headers=self.JSON_HEADER)

        # Check HTTP Status Code is OK (200)
        assert options_request.status_code == requests.codes.ok

        options = options_request.json()

        # Check allowed methods in headers
        methods = options_request.headers[self.KEY_HEADER_ALLOW].split(', ')

        # If we have PUT it means that we can update
        # Let's verify that we have a list of fields for PUT
        if self.KEY_METHOD_PUT in methods:
            assert options[self.KEY_ACTIONS].get(
                self.KEY_METHOD_PUT) is not None

        cpedata.delete()

    @pytest.mark.api
    def test_cpedata_details_get_object(self):
        """
        Checks the controls details GET method
        checks the object exists and return its data.
        """

        # Create a cpe data
        cpedata = good_cpedata()
        cpedata.save()

        # Retrieve GET from API
        endpoint = u'{host}:{port}{api_url}{cpedata_pk}/'.format(
            host=self.BASE_HOST,
            port=self.BASE_PORT,
            api_url=self.BASE_API_URL,
            cpedata_pk=cpedata.pk)
        get_request = requests.get(
            endpoint, headers=self.JSON_HEADER)

        # Check HTTP Status Code is OK (200)
        assert get_request.status_code == requests.codes.ok

        result = get_request.json()

        # Check object corresponds to that from database
        assert cpedata.id == result[self.KEY_ATT_ID]
        assert cpedata.part == result[self.KEY_ATT_PART]
        assert cpedata.vendor == result[self.KEY_ATT_VENDOR]
        assert cpedata.product == result[self.KEY_ATT_PRODUCT]
        assert cpedata.version == result[self.KEY_ATT_VERSION]
        assert cpedata.update == result[self.KEY_ATT_UPDATE]
        assert cpedata.edition == result[self.KEY_ATT_EDITION]
        assert cpedata.sw_edition == result[self.KEY_ATT_SW_EDITION]
        assert cpedata.target_sw == result[self.KEY_ATT_TARGET_SW]
        assert cpedata.target_hw == result[self.KEY_ATT_TARGET_HW]
        assert cpedata.other == result[self.KEY_ATT_OTHER]
        assert cpedata.language == result[self.KEY_ATT_LANGUAGE]

        cpedata.delete()

    @pytest.mark.api
    def test_cpedata_details_put_object_good_fields(self):
        """
        Edits a cpe data with all fields ok.
        """

        # Create a cpe data
        cpedata = good_cpedata()
        cpedata.save()

        # Retrieve GET from API
        endpoint = u'{host}:{port}{api_url}{cpedata_pk}/'.format(
            host=self.BASE_HOST,
            port=self.BASE_PORT,
            api_url=self.BASE_API_URL,
            cpedata_pk=cpedata.pk)
        get_request = requests.get(
            endpoint, headers=self.JSON_HEADER)

        # Check HTTP Status Code is OK (200)
        assert get_request.status_code == requests.codes.ok

        result = get_request.json()

        # We modify some fields from the result
        vendor_edit = u'"testingvendor"'
        result[self.KEY_ATT_VENDOR] = vendor_edit

        # Send PUT request to update object
        put_request = requests.put(
            endpoint, headers=self.JSON_HEADER, data=json.dumps(result))

        put_result = put_request.json()

        # Check HTTP Status Code is OK (200)
        assert put_request.status_code == requests.codes.ok

        # Check the returned object
        assert put_result[self.KEY_ATT_VENDOR] == vendor_edit

        # Get the cpe data again from database
        cpedata_db = CpeData.objects.get(id=cpedata.id)

        assert cpedata_db.vendor == vendor_edit

        cpedata_db.delete()

    @pytest.mark.api
    def test_cpedata_details_put_object_bad_required_fields(self):
        """
        Edits a cpe data and tries to save
        it with some missing fields.
        """

        # Create a cpe data
        cpedata = good_cpedata()
        cpedata.save()

        # Retrieve GET from API
        endpoint = u'{host}:{port}{api_url}{cpedata_pk}/'.format(
            host=self.BASE_HOST,
            port=self.BASE_PORT,
            api_url=self.BASE_API_URL,
            cpedata_pk=cpedata.pk)
        get_request = requests.get(
            endpoint, headers=self.JSON_HEADER)

        # Check HTTP Status Code is OK (200)
        assert get_request.status_code == requests.codes.ok

        result = get_request.json()

        # We modify some fields from the result
        result[self.KEY_ATT_VENDOR] = u''

        # Send PUT request to update object
        put_request = requests.put(
            endpoint, headers=self.JSON_HEADER, data=json.dumps(result))

        error_list = put_request.json()

        # Check HTTP Status Code is OK (200)
        assert put_request.status_code == requests.codes.bad_request

        # Check response error list
        assert error_list.get(self.KEY_ATT_VENDOR) is not None

        cpedata.delete()

    @pytest.mark.api
    def test_cpedata_details_patch_object_good_fields(self):
        """
        Partially edits a cpe data with all fields ok.
        """

        # Create a cpe data
        cpedata = good_cpedata()
        cpedata.save()

        # Patch control
        old_vendor = cpedata.vendor
        new_vendor = u'"NewVendor"'
        patch_cpedata = {self.KEY_ATT_VENDOR: new_vendor}
        detail_endpoint = u'{host}:{port}{api_url}{cpedata_id}/'.format(
            host=self.BASE_HOST,
            port=self.BASE_PORT,
            api_url=self.BASE_API_URL,
            cpedata_id=cpedata.id)

        patch_request = requests.patch(
            detail_endpoint,
            headers=self.JSON_HEADER,
            data=json.dumps(patch_cpedata))

        # Check HTTP Status Code is OK (200)
        assert patch_request.status_code == requests.codes.ok

        result = patch_request.json()

        assert result[self.KEY_ATT_VENDOR] is not old_vendor
        assert result[self.KEY_ATT_VENDOR] == new_vendor

        cpedata.delete()

    @pytest.mark.api
    def test_cpedata_details_patch_object_bad_required_fields(self):
        """
        Partially edits a cpe data missing some fields.
        """

        # Create a cpe data
        cpedata = good_cpedata()
        cpedata.save()

        # Patch cpe data
        new_vendor = u''
        patch_cpedata = {self.KEY_ATT_VENDOR: new_vendor}
        detail_endpoint = u'{host}:{port}{api_url}{cpedata_id}/'.format(
            host=self.BASE_HOST,
            port=self.BASE_PORT,
            api_url=self.BASE_API_URL,
            cpedata_id=cpedata.id)

        patch_request = requests.patch(
            detail_endpoint,
            headers=self.JSON_HEADER,
            data=json.dumps(patch_cpedata))

        # Check HTTP Status Code is Bad Request (400)
        assert patch_request.status_code == requests.codes.bad_request

        error_list = patch_request.json()

        # Check the error list
        assert error_list.get(self.KEY_ATT_VENDOR) is not None

        cpedata.delete()

    @pytest.mark.api
    def test_cpedata_details_delete_object_good_exist(self):
        """
        Deletes an existent cpe data in database.
        """

        # Create a cpe data
        cpedata = good_cpedata()
        cpedata.save()

        detail_endpoint = u'{host}:{port}{api_url}{cpedata_id}/'.format(
            host=self.BASE_HOST,
            port=self.BASE_PORT,
            api_url=self.BASE_API_URL,
            cpedata_id=cpedata.id)

        delete_request = requests.delete(
            detail_endpoint,
            headers=self.JSON_HEADER)

        # Check HTTP Status Code is No Content (204)
        assert delete_request.status_code == requests.codes.no_content

    @pytest.mark.api
    def test_cpedata_details_delete_object_bad_dont_exist(self):
        """
        Tries to delete an inexistent cpe data in database.
        """

        # Create a cpe data
        cpedata = good_cpedata()
        cpedata.save()

        # Delete the cpe data keeping its id
        old_id = cpedata.id
        cpedata.delete()

        detail_endpoint = u'{host}:{port}{api_url}{cpedata_id}/'.format(
            host=self.BASE_HOST,
            port=self.BASE_PORT,
            api_url=self.BASE_API_URL,
            cpedata_id=old_id)

        delete_request = requests.delete(
            detail_endpoint,
            headers=self.JSON_HEADER)

        # Check HTTP Status Code is Not Found (404)
        assert delete_request.status_code == requests.codes.not_found
