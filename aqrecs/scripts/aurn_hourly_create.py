import logging
import sys
from datetime import datetime
from typing import Optional

import pytz
import requests
from bs4 import BeautifulSoup
from pyramid.paster import bootstrap, setup_logging
from sqlalchemy.exc import OperationalError, SQLAlchemyError

from aqrecs.models import AurnHourly, AurnSite
from aqrecs.scripts.aurn_site_data import site_list
from aqrecs.scripts.initialize_db import parse_args

log = logging.getLogger(__name__)


def create_hourly_records(dbsession):
    """
    Creates a aurn_hourly_table record for each site in a list, represented
    by string names
    """
    page = requests.get('https://uk-air.defra.gov.uk/latest/currentlevels',
                        headers={'User-Agent': 'Not blank'}).content
    soup = BeautifulSoup(page, 'lxml')
    for site_name in site_list:
        try:
            site_id = dbsession.query(AurnSite.id).filter(
                AurnSite.name == site_name).one()[0]
        except SQLAlchemyError as e:
            log.error(f'Site name: {site_name} -- {e}')
            continue

        hourly_data = get_hourly_data(soup, site_name)
        if not hourly_data:
            continue
        record = AurnHourly(site_id=site_id, **hourly_data)
        dbsession.add(record)


def get_hourly_data(soup, site_name: str) -> Optional[dict]:
    if soup.find_all('a', string=site_name):
        site_link = soup.find_all('a', string=site_name)[0]
        row = site_link.findParent('td').findParent('tr').findAll('td')
        try:
            time_str = row[6].text[:10] + ' ' + row[6].text[10:15]
        except IndexError:
            log.debug(f'IndexError catch for site name: {site_name} row: {row}')
            return None
        try:
            dt = datetime.strptime(time_str.replace('24:00', '00:00'),
                                   '%d/%m/%Y %H:%M')
        except ValueError as e:
            log.debug(f'ValueError catch for site name: {site_name}')
            log.debug(e)
            return None
        if not time_is_current(dt):
            log.debug(f'not time_is_current for site name: {site_name}')
            return None

        aq_values = [row[n].text.replace('\xa0', ' ').split(' ')[0]
                     for n in range(1, 6)]
        for ind, val in enumerate(aq_values):
            try:
                aq_values[ind] = int(val)
            except ValueError:
                if val not in ['', 'n/a', 'n/m']:
                    log.debug(f'not in condition for site name: {site_name}')
                    log.debug(f'val is {val}')
                aq_values[ind] = None
        hourly_data = dict(zip(['ozone', 'no2', 'so2', 'pm25', 'pm10'],
                               aq_values))
        hourly_data['time'] = dt
        return hourly_data


def time_is_current(record_dt):
    loc_dt = pytz.timezone('Europe/London').localize(datetime.now())
    time_str = datetime.strftime(loc_dt.replace(
        microsecond=0, second=0, minute=0), "%d/%m/%Y %H:%M")
    if record_dt.strftime('%d/%m/%Y %H:%M') == time_str:
        return True
    log.debug(f'not current; record_dt is: {record_dt}  loc dt is {loc_dt}')


def main(argv=sys.argv):
    args = parse_args(argv)
    setup_logging(args.config_uri)
    env = bootstrap(args.config_uri)
    try:
        with env['request'].tm:
            dbsession = env['request'].dbsession
            create_hourly_records(dbsession)
    except OperationalError:
        print('''
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.md for description and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.
            ''')
