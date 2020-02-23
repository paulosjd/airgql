from pyramid.view import view_config
from sqlalchemy import desc

from aqrecs.models import AurnHourly


@view_config(route_name='site_aq_data', renderer='json')
def site_aq_data(request):
    try:
        site_id = int(request.matchdict.get('site_id', ''))
    except ValueError:
        return []

    results = request.dbsession.query(AurnHourly).filter(
        AurnHourly.site_id == site_id,
    ).order_by(
        desc(AurnHourly.time)
    )

    site_aqs = [
        {**{k: getattr(a, k) for k in ['pm10', 'pm25', 'no2', 'ozone']},
         'time': a.time.isoformat()}
        for a in results.all()
    ]

    return {'aq_data': site_aqs, 'site_id': site_id}
