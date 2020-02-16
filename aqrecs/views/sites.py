from pyramid.view import view_config
from sqlalchemy import desc

from aqrecs.models import AurnHourly, AurnSite


@view_config(route_name='sites', renderer='json')
def sites_view(request):
    aq_fields = ['pm10', 'pm25', 'no2', 'ozone']
    sites_query = request.dbsession.query(AurnSite)

    t_subq = request.dbsession.query(AurnHourly.time).order_by(
        desc(AurnHourly.time)
    ).limit(1).scalar()
    recent_aq = request.dbsession.query(AurnHourly).filter(
        AurnHourly.time == t_subq)
    site_aqs = {
        a.site_id: {k: getattr(a, k) for k in aq_fields}
        for a in recent_aq
    }

    return [
        site.serialize(
            extras=site_aqs.get(site.id, {k: None for k in aq_fields})
        ) for site in sites_query.all()
    ]

"""

recent_aq_query = request.dbsession.query(AurnHourly).filter(AurnHourly.time == lat_time_rec.time)
print('1')
print(str(recent_aq_query))
t_subq = request.dbsession.query(AurnHourly.time).order_by(desc(AurnHourly.time)).limit(1).scalar()
recent_aq_query2 = request.dbsession.query(AurnHourly).filter(AurnHourly.time == t_subq)
print('2')
print(str(recent_aq_query2))
        
1
SELECT aurn_hourly.id AS aurn_hourly_id, aurn_hourly.time AS aurn_hourly_time, aurn_hourly.site_id AS aurn_hourly_site_id, aurn_hourly.ozone AS aurn_hourly_ozone, aurn_hourly.no
2 AS aurn_hourly_no2, aurn_hourly.so2 AS aurn_hourly_so2, aurn_hourly.pm25 AS aurn_hourly_pm25, aurn_hourly.pm10 AS aurn_hourly_pm10
FROM aurn_hourly
WHERE aurn_hourly.time = %(time_1)s
2
SELECT aurn_hourly.id AS aurn_hourly_id, aurn_hourly.time AS aurn_hourly_time, aurn_hourly.site_id AS aurn_hourly_site_id, aurn_hourly.ozone AS aurn_hourly_ozone, aurn_hourly.no
2 AS aurn_hourly_no2, aurn_hourly.so2 AS aurn_hourly_so2, aurn_hourly.pm25 AS aurn_hourly_pm25, aurn_hourly.pm10 AS aurn_hourly_pm10
FROM aurn_hourly
WHERE aurn_hourly.time = %(time_1)s
"""
