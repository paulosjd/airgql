import unittest
from collections import namedtuple
from unittest.mock import patch

from graphql import GraphQLError
from pyrasatest import MockQuery

from aqrecs.schema import Query


aurn_site_type_fields = 'id', 'name', 'region',
aurn_site_type_meta = namedtuple('meta_mock', 'fields')(aurn_site_type_fields)


class SchemaTestCase(unittest.TestCase):

    @patch('aqrecs.schema.Query.get_site_filter_kwargs_dict', return_value=None)
    def test_resolve_hourly_data_where_get_site_filter_kwargs_dict_returns_none(
            self, get_filter_dict_patch
    ):
        with self.assertRaises(GraphQLError):
            Query.resolve_hourly_data('root', 'info'),

    @patch('aqrecs.schema.Query.get_aurn_sites')
    @patch('aqrecs.schema.Query.get_site_filter_kwargs_dict')
    @patch('aqrecs.schema.AurnHourlyType.get_query')
    @patch('aqrecs.schema.AurnHourly')
    @patch('aqrecs.schema.get_time_filter_params')
    def test_resolve_hourly_data_where_site_ids_provided(
            self, get_times_patch, aurn_hourly_patch, get_query_patch,
            get_filter_dict_patch, get_sites_patch
    ):
        get_times_patch.return_value = 1, 3
        aurn_hourly_patch.time = 2
        aurn_hourly_patch.site_id = namedtuple('sa_obj', 'in_')(lambda x: x)
        sites_query_ids = [5, 6, 7]
        get_sites_patch.return_value = [
            namedtuple('site', 'id')(i) for i in sites_query_ids
        ]
        test_val = 'expected_return_val'
        mock_query = MockQuery(all_=test_val)
        get_query_patch.return_value = mock_query
        site_ids_queried = [3, 5, 6, 25]
        self.assertEqual(
            test_val,
            Query.resolve_hourly_data('root', 'info', site_ids=site_ids_queried)
        )
        self.assertEqual(
            (aurn_hourly_patch.time >= get_times_patch.return_value[0],
             aurn_hourly_patch.time <= get_times_patch.return_value[1],
             [i for i in sites_query_ids if i in site_ids_queried]),
            mock_query.filter_args
        )

    @patch('aqrecs.schema.Query.get_aurn_sites')
    @patch('aqrecs.schema.Query.get_site_filter_kwargs_dict')
    @patch('aqrecs.schema.AurnHourlyType.get_query')
    @patch('aqrecs.schema.AurnHourly')
    @patch('aqrecs.schema.get_time_filter_params')
    def test_resolve_hourly_data_where_not_site_ids(
            self, get_times_patch, aurn_hourly_patch, get_query_patch,
            get_filter_dict_patch, get_sites_patch
    ):
        get_sites_patch.return_value = [namedtuple('site', 'id')(5)]
        get_times_patch.return_value = 1, 3
        aurn_hourly_patch.time = 2
        aurn_hourly_patch.site_id = namedtuple('sa_obj', 'in_')(lambda x: x)
        test_val = 'expected_return_val'
        mock_query = MockQuery(all_=test_val)
        get_query_patch.return_value = mock_query
        self.assertEqual(
            test_val,
            Query.resolve_hourly_data('root', 'info', foo='bar')
        )
        self.assertEqual(
            (aurn_hourly_patch.time >= get_times_patch.return_value[0],
             aurn_hourly_patch.time <= get_times_patch.return_value[1],
             [a.id for a in get_sites_patch.return_value]),
            mock_query.filter_args
        )

    @patch('aqrecs.schema.Query.get_site_filter_kwargs_dict')
    @patch('aqrecs.schema.Query.get_aurn_sites')
    def test_resolve_sites_where_filter_kwargs_not_none(
            self, get_aurn_sites_patch, get_filter_dict_patch
    ):
        kwargs = {k: k[:3] for k in ['latitude', 'longitude']}
        geo = [kwargs[k] for k in ['latitude', 'longitude']]
        filter_kwargs_dct = {}
        get_filter_dict_patch.return_value = filter_kwargs_dct
        self.assertEqual(
            get_aurn_sites_patch.return_value,
            Query.resolve_sites('root', 'info', **kwargs)
        )
        get_aurn_sites_patch.assert_called_with(
            'info', filter_kwargs_dct, geo, geo_limit=kwargs.get('geo_limit_by')
        )

    @patch('aqrecs.schema.Query.get_site_filter_kwargs_dict', return_value=None)
    def test_resolve_sites_where_filter_kwargs_is_none(self, get_filt_dct_pch):
        with self.assertRaises(GraphQLError):
            Query.resolve_sites('root', 'info')

    @patch('aqrecs.schema.AurnRegions.get_value_from_name', return_value=None)
    @patch('aqrecs.schema.AurnSiteType._meta', new=aurn_site_type_meta)
    def test_get_site_filter_kwargs_dict_where_get_value_from_name_returns_none(
            self, get_value_from_name_patch
    ):
        input_kwargs = {k: f'{k}_val' for k in aurn_site_type_meta.fields}
        self.assertIsNone(Query.get_site_filter_kwargs_dict(input_kwargs))

    @patch('aqrecs.schema.AurnRegions.get_value_from_name')
    @patch('aqrecs.schema.AurnSiteType._meta', new=aurn_site_type_meta)
    def test_get_site_filter_kwargs_dict(self, get_value_from_name_patch):

        initial_kwargs = {k: f'{k}_val' for k in aurn_site_type_meta.fields}
        initial_kwargs['foo'] = 'bar'

        expected_output = {k: v for k, v in initial_kwargs.items()
                           if k in aurn_site_type_meta.fields and k != 'region'}
        expected_output['region'] = get_value_from_name_patch.return_value

        self.assertEqual(
            expected_output,
            Query.get_site_filter_kwargs_dict(initial_kwargs)
        )

    @patch('aqrecs.schema.AurnSiteType.get_query')
    @patch('aqrecs.schema.haversine')
    def test_get_aurn_sites_all_geo_and_geo_limit(self, haversine_patch,
                                                  get_query_patch):
        site_items = ['b', 'c', 'a'] + ['s' for _ in range(20)]
        sort_keys = ['3', '1', '2'] + ['4' for _ in range(20)]
        haversine_patch.side_effect = [s for s in sort_keys]
        get_query_patch.return_value = MockQuery(all_=site_items)
        geo_lim = 15

        output = Query.get_aurn_sites({}, {}, ['lat', 'lon'], geo_limit=geo_lim)
        self.assertEqual(
            list(sorted(
                site_items, key=lambda x: sort_keys[site_items.index(x)]
            ))[:geo_lim],
            output
        )

    @patch('aqrecs.schema.AurnSiteType.get_query')
    @patch('aqrecs.schema.haversine')
    def test_get_aurn_sites_all_geo_not_geo_limit(self, haversine_patch,
                                                  get_query_patch):
        site_items = ['b', 'c', 'a'] + ['s' for _ in range(20)]
        sort_keys = ['3', '1', '2'] + ['s' for _ in range(20)]
        haversine_patch.side_effect = [s for s in sort_keys]
        get_query_patch.return_value = MockQuery(all_=site_items)

        output = Query.get_aurn_sites({}, {}, ['lat', 'lon'])
        self.assertEqual(
            list(sorted(site_items,
                        key=lambda x: sort_keys[site_items.index(x)])),
            output
        )

    @patch('aqrecs.schema.AurnSiteType.get_query')
    def test_get_aurn_sites_not_all_geo(self, get_query_patch):
        site_items = 'all'
        get_query_patch.return_value = MockQuery(all_=site_items)
        output = Query.get_aurn_sites({}, {}, [0, 0])
        self.assertEqual(site_items, output)


if __name__ == '__main__':
    unittest.main()
