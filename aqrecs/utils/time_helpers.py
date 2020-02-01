from datetime import datetime, timedelta
from typing import List

import pytz

DEFAULT_HOURS = 72


def get_time_filter_params(kwargs: dict) -> List[datetime]:
    """ Returns list with tz-aware datetime for the start date at index
    position 0 and end date at index position 1 """

    items = [('start_date', kwargs.get('hours', DEFAULT_HOURS)),
             ('end_date', 0)]
    times = [kwargs.get(a, '').replace('T', ' ').replace('/', '-')[:16]
             for a, b in items]

    dts = []
    for ind, time in enumerate(times):
        if time:
            dt_fmt = '%Y-%m-%d %H:%M' if len(time) == 16 else '%Y-%m-%d'
            try:
                time = datetime.strptime(time, dt_fmt)
            except ValueError:
                time = None
        if not time:
            loc_dt = pytz.timezone('Europe/London').localize(
                datetime.now()).replace(microsecond=0, second=0, minute=0)
            time = loc_dt - timedelta(hours=items[ind][1])
        dts.append(time)

    return dts
