import json
import unittest
from datetime import datetime
from collections import namedtuple
from unittest.mock import patch, PropertyMock

from bs4 import BeautifulSoup
from pyrasatest import MockModel, MockQuery, MockRequest, MockDbSession
from sqlalchemy.exc import SQLAlchemyError

from aqrecs.scripts.aurn_hourly_create import (
    create_hourly_records, get_hourly_data, time_is_current
)


path = 'aqrecs.scripts.aurn_hourly_create'

expected_return_val = {
    'ozone': 80, 'no2': 3, 'so2': None, 'pm25': None, 'pm10': None,
    'time': datetime(2020, 1, 30, 22, 0)
}


class AurnHourlyCreateTestCase(unittest.TestCase):

    def setUp(self):
        self.site_name = 'Fort William'
        self.html = """
        <tr><td><a href="../networks/site-info?site_id=FW">{}</a><br/>
        <a>Timeseries Graph</a></td><td><span>80 (3 Low)</span></td><td>
        <span>3 (1 Low)</span></td><td><span>n/m</span></td><td><span>n/m</span>
        </td><td><span>n/m</span></td><td>30/01/2020<br/>22:00</td></tr>
        """.format(self.site_name)

    @patch(f'{path}.AurnHourly')
    @patch(f'{path}.get_hourly_data')
    @patch(f'{path}.requests.get')
    @patch(f'{path}.site_list', new=[f'site_{s}' for s in ['a', 'b', 'c']])
    def test_create_hourly_records(self, req_get_patch,
                                   get_hourly_data_patch, model_patch):
        req_get_patch.return_value = namedtuple('req_get', 'content')('')
        site_id = 5
        dbsession = MockDbSession(side_effect=[
            MockQuery(raise_exc=SQLAlchemyError),
            MockQuery(one_=[0]),
            MockQuery(one_=[site_id]),
        ])
        hourly_data = {'foo': 'bar'}
        get_hourly_data_patch.side_effect = [{}, hourly_data]
        create_hourly_records(dbsession)
        model_patch.assert_called_with(site_id=site_id, **hourly_data)
        self.assertEqual([model_patch.return_value], dbsession.added_records)

    def test_get_hourly_data_soup_no_find(self):
        test_soup = BeautifulSoup(self.html, 'lxml')
        self.assertIsNone(get_hourly_data(test_soup, site_name='foo'))

    def test_get_hourly_data_index_error_condition(self):
        test_soup = BeautifulSoup(
            self.html.replace('<td>30/01/2020<br/>22:00</td></tr>', ''), 'lxml'
        )
        self.assertIsNone(get_hourly_data(test_soup, site_name=self.site_name))

    @patch(f'{path}.time_is_current', return_value=False)
    def test_get_hourly_data_time_not_is_current_condition(self, tic_pch):
        test_soup = BeautifulSoup(self.html, 'lxml')
        self.assertIsNone(get_hourly_data(test_soup, site_name=self.site_name))

    @patch(f'{path}.time_is_current', return_value=True)
    def test_get_hourly_data_gives_expected_output(self, tic_pch):
        test_soup = BeautifulSoup(self.html, 'lxml')
        site_link = test_soup.find_all('a', string=self.site_name)[0]
        row = site_link.findParent('td').findParent('tr').findAll('td')
        aq_values = [row[n].text.split('\xa0')[0] for n in range(1, 6)]
        for ind, val in enumerate(aq_values):
            if val.startswith('n/m'):
                aq_values[ind] = None
            else:
                aq_values[ind] = int(val)
        expected_output = dict(zip(['ozone', 'no2', 'so2', 'pm25', 'pm10'],
                               aq_values))
        expected_output['time'] = datetime(2020, 1, 30, 22)
        self.assertEqual(expected_output,
                         get_hourly_data(test_soup, site_name=self.site_name))



if __name__ == '__main__':
    unittest.main()
