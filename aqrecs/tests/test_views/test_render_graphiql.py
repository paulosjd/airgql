import json
import unittest
from collections import namedtuple
from unittest.mock import patch

from pyramid.exceptions import HTTPNotFound
from pyramid.response import Response
from pyramid.testing import DummyRequest

from aqrecs.views.render_graphiql import render_graphiql


class RenderGraphiQLTestCase(unittest.TestCase):

    def setUp(self):
        self.view = render_graphiql
        self.request = DummyRequest()
        self.request.dbsession = ''
        self.request.registry.settings = {}

    def test_render_graphiql_view_settings_raise_http_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.view(self.request)

    @patch('aqrecs.views.render_graphiql.aurn_sites_schema.execute')
    @patch('aqrecs.views.render_graphiql.render', return_value='')
    def test_json_body_key_error_condition(self, render_patch, schema_patch):
        self.request.json_body = {}
        self.request.registry.settings = {'graphiql_enabled': 'true'}
        self.assertIsInstance(self.view(self.request), Response)
        render_patch.assert_called_with(
            '../templates/graphiql.mako', {}, self.request
        )

    @patch('aqrecs.views.render_graphiql.aurn_sites_schema.execute')
    @patch('aqrecs.views.render_graphiql.render', return_value='')
    def test_data_attribute_truthy_condition(self, render_patch, schema_patch):
        self.request.json_body = {'query': 'q'}
        self.request.registry.settings = {'graphiql_enabled': 'true'}
        Result = namedtuple('result_obj', 'data')
        data = {'foo': 'bar'}
        schema_patch.return_value = Result(data)
        output = self.view(self.request)
        self.assertEqual(json.dumps(data).encode(), output.body)

    @patch('aqrecs.views.render_graphiql.aurn_sites_schema.execute')
    @patch('aqrecs.views.render_graphiql.render', return_value='')
    def test_data_attribute_falsey_condition(self, render_patch, schema_patch):
        self.request.json_body = {'query': 'q'}
        self.request.registry.settings = {'graphiql_enabled': 'true'}
        Result = namedtuple('result_obj', ['data', 'errors'])
        errors_list = ['foo', 'bar']
        schema_patch.return_value = Result({}, errors_list)
        output = self.view(self.request)
        self.assertEqual(
            json.dumps([{'message': str(i)} for i in errors_list]).encode(),
            output.body
        )
